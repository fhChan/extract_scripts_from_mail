/**
 * Created by Administrator on 8/1/2016.
 */

esprima = require("esprima");
estraverse = require("estraverse");
escodegen = require("escodegen");

function process_script(script_content) {
    // console.log(script_content);
    var ast = esprima.parse(script_content);
    //console.log(ast);

    var var_decls_map = {};
    function search_name_in_map(name) {
        for (decl in var_decls_map) {
            if (decl == name) {
                return var_decls_map[decl];
            }
        }
        return undefined;
    }

    var func_name_list = [];
    function search_func_name_in_list(name) {
        for (var i = 0; i < func_name_list.length; ++i) {
            if (name == func_name_list[i]) {
                return true;
            }
        }
        return false;
    }

    //
    estraverse.traverse(ast, {
        enter: function (node, parent) {
            try {
                switch (node.type) {
                    case esprima.Syntax.VariableDeclaration: {
                        for (index in node.declarations) {
                            var decl = node.declarations[index];
                            //
                            // Sample Code:
                            // var GtDEcTuuN = WScript.CreateObject('WScript.shell');
                            // var TkTuwCGFLuv_save = GtDEcTuuN.SpecialFolders('MyDocuments');
                            //  ==>
                            // var wscript_shell_ = WScript.CreateObject('WScript.shell');
                            // var TkTuwCGFLuv_save = wscript_shell_.SpecialFolders('MyDocuments');
                            //
                            // Sample Code:
                            // var WSseCXFVG = new ActiveXObject('WbemScripting.SWbemLocator');
                            // var rXRUTkui = WSseCXFVG.ConnectServer(strComputer, 'root\\default');
                            // ==>
                            // var wbemscripting_swbemlocator_ = new ActiveXObject('WbemScripting.SWbemLocator');
                            // var rXRUTkui = wbemscripting_swbemlocator_.ConnectServer(strComputer, 'root\\default');
                            //
                            if (decl.type == esprima.Syntax.VariableDeclarator
                                && ((decl.init.type == esprima.Syntax.CallExpression
                                && decl.init.callee.type == esprima.Syntax.MemberExpression
                                && decl.init.callee.object.type == esprima.Syntax.Identifier)
                                || (decl.init.type == esprima.Syntax.NewExpression))
                                && decl.init.arguments[0].type == esprima.Syntax.Literal
                            ) {
                                var new_name = decl.init.arguments[0].value.toLowerCase().replace('.', '_') + '_';
                                var_decls_map[decl.id.name] = new_name;
                                decl.id.name = new_name;
                            }

                            //
                            // Customized function
                            //
                            // variable declaration for function
                            // example: var f489hir = function  () {};
                            //
                            if (decl.type == esprima.Syntax.VariableDeclarator
                                && decl.id.type == esprima.Syntax.Identifier
                                && decl.init.type == esprima.Syntax.FunctionExpression) {
                                func_name_list.push(decl.id.name);
                                eval.call(global, escodegen.generate(decl));
                            }
                        }
                        break;
                    }
                    case esprima.Syntax.FunctionDeclaration: {
                        //
                        // Customized function
                        //
                        // variable declaration for function
                        // example: function f489hir () {};
                        //
                        /*
                        if (node.id.type == esprima.Syntax.Identifier) {
                            func_name_list.push(node.id.name);
                            eval.call(global, escodegen.generate(node));
                        }
                        */
                        break;
                    }
                    case esprima.Syntax.ExpressionStatement: {
                        //
                        // Sample Code:
                        // var DmYbWSaT;
                        // DmYbWSaT = new ActiveXObject('Scripting.FileSystemObject');
                        // e = new Enumerator(DmYbWSaT.Drives);
                        // ==>
                        // scripting_filesystemobject_ = new ActiveXObject('Scripting.FileSystemObject');
                        // e = new Enumerator(scripting_filesystemobject_.Drives);
                        //
                        if (node.expression.type == esprima.Syntax.AssignmentExpression
                            && node.expression.right.type == esprima.Syntax.NewExpression
                            && node.expression.right.arguments[0].type == esprima.Syntax.Literal
                            && node.expression.left.type == esprima.Syntax.Identifier
                        ) {
                            var old_name = node.expression.left.name;
                            var new_name = node.expression.right.arguments[0].value.toLowerCase().replace('.', '_') + '_';
                            var_decls_map[old_name] = new_name;
                            node.expression.left.name = new_name;
                        }
                        //
                        // customized function, sample code:
                        // var f489hir;
                        // f489hir = function(i9j5g1mf3n) {
                        //     var j0v8n6n8oi = "",
                        //         tk89p583 = i9j5g1mf3n.match(/(..)/g);
                        //     for (var i = 0; i < tk89p583.length; i++) j0v8n6n8oi += String.fromCharCode(parseInt(tk89p583[i], 17));
                        //     return j0v8n6n8oi
                        // };
                        // wuhl3uu7 = window[f489hir("4f5e6c636a6e41686163685g3f6f63665f515g6c6d636968")]();
                        //
                        if (node.expression.type == esprima.Syntax.AssignmentExpression
                            && node.expression.right.type == esprima.Syntax.FunctionExpression) {
                            func_name_list.push(node.expression.left.name);
                            var func_decl = escodegen.generate(node);
                            eval.call(global, func_decl);
                        }
                        break;
                    }
                    case esprima.Syntax.Identifier: {
                        var new_name = search_name_in_map(node.name);
                        if (new_name != undefined) {
                            node.name = new_name;
                        }
                        break;
                    }
                }
            } catch (err) {
                console.error(err);
            }

        },
        leave: function (node, parent) {
            //console.log(node.type);
        }
    });

    ast = estraverse.replace(ast, {
        enter: function (node, parent) {
        },
        leave: function (node, parent) {
            switch (node.type) {
                case esprima.Syntax.CallExpression: {
                    var call_exp = escodegen.generate(node);
                    var ret_val;
                    try {
                        ret_val = eval.call(global, call_exp);
                        if (ret_val == undefined) break;
                        return {
                            type: esprima.Syntax.Literal,
                            value: ret_val,
                            raw: ret_val
                        };
                    } catch (err) {
                        console.error("Error in calculate call_exp: " + err);
                    }
                    break;
                }
                case esprima.Syntax.BinaryExpression: {
                    if (node.left.type == esprima.Syntax.Literal && node.right.type == esprima.Syntax.Literal) {
                        var ret_val = eval.call(global, escodegen.generate(node));
                        return {
                            type: esprima.Syntax.Literal,
                            value: ret_val,
                            raw: ret_val
                        };
                    }
                    break;
                }
                case esprima.Syntax.MemberExpression: {
                    if (node.computed == true && typeof node.property != "undefined" && node.property.type != esprima.Syntax.Literal) {
                        var property_exp = escodegen.generate(node.property);
                        try {
                            var property_val = eval.call(global, property_exp);
                            if (property_val != undefined) {
                                node.property = {
                                    type: esprima.Syntax.Literal,
                                    value: property_val,
                                    raw: property_val
                                };
                            }
                        } catch (err) {
                            console.error("Error in calculate property_exp: " + err);
                        }
                    }
                    break;
                }
                case esprima.Syntax.VariableDeclaration: {
                    break;
                }
                default: {
                    break;
                }
            }
        },
    });

    console.log(escodegen.generate(ast));
}


function main(filename) {
    var fs = require('fs');
    fs.readFile(filename, 'utf8', function (err, data) {
        if (err) throw err;
        process_script(data);
    });
}

main(process.argv[2]);
