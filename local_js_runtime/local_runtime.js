var tmsaScriptShell = {
  run : function() {
    console.log("[WScript.Shell] run");
  },
  Run : function(cmd, style, wait_on_return) {
    console.log("[WScript.Shell] Run! CMD: " + cmd + ", Window Style: " + style + ", Wait on return: " + wait_on_return);
  },
  ExpandEnvironmentStrings : function(path) {
    console.log("[WScript.Shell] ExpandEnvironmentStrings, path = " + path);
    return path;
  }
}

var tmsaXMLHttp = {
  open : function(method, url, async=true, username="", password="") {
    console.log("[XMLHttpRequest] open HTTP request, method = " + method + ", URL = " + url);
  },
  send : function() {
    console.log("[XMLHttpRequest] send HTTP request");
  },
  get status() {
    console.log("[XMLHttpRequest] get HTTP status, return 200");
    return 200;
  },
  get ResponseBody() {
    console.log("[XMLHttpRequest] get HTTP Response Body");
    return "fake_response_body_content";
  }
}

var tmsaADODB = {
  open : function() {
    console.log("[ADODB.Stream] open stream");
  },
  write : function(args) {
    console.log("[ADODB.Stream] write content, " + args);
  },
  saveToFile : function(args) {
    console.log("[ADODB.Stream] save to file, path = " + args);
  },
  SaveToFile : function(file_name, save_options) {
    console.log("[ADODB.Stream][SaveToFile] save to file, path = " + file_name + ", options = " + save_options);
  },
  close : function() {
    console.log("[ADODB.Stream] close stream");
  }, 
  set type(val) {
    console.log("[ADODB.Stream] set type, value = " + val);
  },
  set position(val) {
    console.log("[ADODB.Stream] set position, value = " + val);
  }
}

ActiveXObject = function (name) {
  switch (name) {
    case "WScript.Shell":
      console.log("[ActiveXObject] create WScript.Shell");
      return tmsaScriptShell;
    case "MSXML2.XMLHTTP":
      console.log("[ActiveXObject] create MSXML2.XMLHTTP");
      return tmsaXMLHttp;
    case "ADODB.Stream":
      console.log("[ActiveXObject] create ADODB.Stream");
      return tmsaADODB;
  }
}

function execute() {
  //wscript = new ActiveXObject("WScript.Shell");
  //wscript.run();
}

var WScript = {
  CreateObject : function(val) {
    console.log("[WScript] create object, name = " + val);
    return ActiveXObject(val);
  },
  Sleep : function(milliseconds) {
    console.log("[WScript] sleep, milliseconds = " + milliseconds);
  }
}