var TMSA_OP_MAP = [];
TMSA_OP_MAP[TMSA_OP_MAP["bkpt"] = 0x01] = "bkpt";
TMSA_OP_MAP[TMSA_OP_MAP["nop"] = 0x02] = "nop";
TMSA_OP_MAP[TMSA_OP_MAP["throw"] = 0x03] = "throw";
TMSA_OP_MAP[TMSA_OP_MAP["getsuper"] = 0x04] = "getsuper";
TMSA_OP_MAP[TMSA_OP_MAP["setsuper"] = 0x05] = "setsuper";
TMSA_OP_MAP[TMSA_OP_MAP["dxns"] = 0x06] = "dxns";
TMSA_OP_MAP[TMSA_OP_MAP["dxnslate"] = 0x07] = "dxnslate";
TMSA_OP_MAP[TMSA_OP_MAP["kill"] = 0x08] = "kill";
TMSA_OP_MAP[TMSA_OP_MAP["label"] = 0x09] = "label";
TMSA_OP_MAP[TMSA_OP_MAP["lf32x4"] = 0x0A] = "lf32x4";
TMSA_OP_MAP[TMSA_OP_MAP["sf32x4"] = 0x0B] = "sf32x4";
TMSA_OP_MAP[TMSA_OP_MAP["ifnlt"] = 0x0C] = "ifnlt";
TMSA_OP_MAP[TMSA_OP_MAP["ifnle"] = 0x0D] = "ifnle";
TMSA_OP_MAP[TMSA_OP_MAP["ifngt"] = 0x0E] = "ifngt";
TMSA_OP_MAP[TMSA_OP_MAP["ifnge"] = 0x0F] = "ifnge";
TMSA_OP_MAP[TMSA_OP_MAP["jump"] = 0x10] = "jump";
TMSA_OP_MAP[TMSA_OP_MAP["iftrue"] = 0x11] = "iftrue";
TMSA_OP_MAP[TMSA_OP_MAP["iffalse"] = 0x12] = "iffalse";
TMSA_OP_MAP[TMSA_OP_MAP["ifeq"] = 0x13] = "ifeq";
TMSA_OP_MAP[TMSA_OP_MAP["ifne"] = 0x14] = "ifne";
TMSA_OP_MAP[TMSA_OP_MAP["iflt"] = 0x15] = "iflt";
TMSA_OP_MAP[TMSA_OP_MAP["ifle"] = 0x16] = "ifle";
TMSA_OP_MAP[TMSA_OP_MAP["ifgt"] = 0x17] = "ifgt";
TMSA_OP_MAP[TMSA_OP_MAP["ifge"] = 0x18] = "ifge";
TMSA_OP_MAP[TMSA_OP_MAP["ifstricteq"] = 0x19] = "ifstricteq";
TMSA_OP_MAP[TMSA_OP_MAP["ifstrictne"] = 0x1A] = "ifstrictne";
TMSA_OP_MAP[TMSA_OP_MAP["lookupswitch"] = 0x1B] = "lookupswitch";
TMSA_OP_MAP[TMSA_OP_MAP["pushwith"] = 0x1C] = "pushwith";
TMSA_OP_MAP[TMSA_OP_MAP["popscope"] = 0x1D] = "popscope";
TMSA_OP_MAP[TMSA_OP_MAP["nextname"] = 0x1E] = "nextname";
TMSA_OP_MAP[TMSA_OP_MAP["hasnext"] = 0x1F] = "hasnext";
TMSA_OP_MAP[TMSA_OP_MAP["pushnull"] = 0x20] = "pushnull";
TMSA_OP_MAP[TMSA_OP_MAP["c"] = 33] = "c";
TMSA_OP_MAP[TMSA_OP_MAP["pushundefined"] = 0x21] = "pushundefined";
TMSA_OP_MAP[TMSA_OP_MAP["pushfloat"] = 0x22] = "pushfloat";
TMSA_OP_MAP[TMSA_OP_MAP["nextvalue"] = 0x23] = "nextvalue";
TMSA_OP_MAP[TMSA_OP_MAP["pushbyte"] = 0x24] = "pushbyte";
TMSA_OP_MAP[TMSA_OP_MAP["pushshort"] = 0x25] = "pushshort";
TMSA_OP_MAP[TMSA_OP_MAP["pushtrue"] = 0x26] = "pushtrue";
TMSA_OP_MAP[TMSA_OP_MAP["pushfalse"] = 0x27] = "pushfalse";
TMSA_OP_MAP[TMSA_OP_MAP["pushnan"] = 0x28] = "pushnan";
TMSA_OP_MAP[TMSA_OP_MAP["pop"] = 0x29] = "pop";
TMSA_OP_MAP[TMSA_OP_MAP["dup"] = 0x2A] = "dup";
TMSA_OP_MAP[TMSA_OP_MAP["swap"] = 0x2B] = "swap";
TMSA_OP_MAP[TMSA_OP_MAP["pushstring"] = 0x2C] = "pushstring";
TMSA_OP_MAP[TMSA_OP_MAP["pushint"] = 0x2D] = "pushint";
TMSA_OP_MAP[TMSA_OP_MAP["pushuint"] = 0x2E] = "pushuint";
TMSA_OP_MAP[TMSA_OP_MAP["pushdouble"] = 0x2F] = "pushdouble";
TMSA_OP_MAP[TMSA_OP_MAP["pushscope"] = 0x30] = "pushscope";
TMSA_OP_MAP[TMSA_OP_MAP["pushnamespace"] = 0x31] = "pushnamespace";
TMSA_OP_MAP[TMSA_OP_MAP["hasnext2"] = 0x32] = "hasnext2";
TMSA_OP_MAP[TMSA_OP_MAP["li8"] = 0x35] = "li8";
TMSA_OP_MAP[TMSA_OP_MAP["li16"] = 0x36] = "li16";
TMSA_OP_MAP[TMSA_OP_MAP["li32"] = 0x37] = "li32";
TMSA_OP_MAP[TMSA_OP_MAP["lf32"] = 0x38] = "lf32";
TMSA_OP_MAP[TMSA_OP_MAP["lf64"] = 0x39] = "lf64";
TMSA_OP_MAP[TMSA_OP_MAP["si8"] = 0x3A] = "si8";
TMSA_OP_MAP[TMSA_OP_MAP["si16"] = 0x3B] = "si16";
TMSA_OP_MAP[TMSA_OP_MAP["si32"] = 0x3C] = "si32";
TMSA_OP_MAP[TMSA_OP_MAP["sf32"] = 0x3D] = "sf32";
TMSA_OP_MAP[TMSA_OP_MAP["sf64"] = 0x3E] = "sf64";
TMSA_OP_MAP[TMSA_OP_MAP["newfunction"] = 0x40] = "newfunction";
TMSA_OP_MAP[TMSA_OP_MAP["call"] = 0x41] = "call";
TMSA_OP_MAP[TMSA_OP_MAP["construct"] = 0x42] = "construct";
TMSA_OP_MAP[TMSA_OP_MAP["callmethod"] = 0x43] = "callmethod";
TMSA_OP_MAP[TMSA_OP_MAP["callstatic"] = 0x44] = "callstatic";
TMSA_OP_MAP[TMSA_OP_MAP["callsuper"] = 0x45] = "callsuper";
TMSA_OP_MAP[TMSA_OP_MAP["callproperty"] = 0x46] = "callproperty";
TMSA_OP_MAP[TMSA_OP_MAP["returnvoid"] = 0x47] = "returnvoid";
TMSA_OP_MAP[TMSA_OP_MAP["returnvalue"] = 0x48] = "returnvalue";
TMSA_OP_MAP[TMSA_OP_MAP["constructsuper"] = 0x49] = "constructsuper";
TMSA_OP_MAP[TMSA_OP_MAP["constructprop"] = 0x4A] = "constructprop";
TMSA_OP_MAP[TMSA_OP_MAP["callsuperid"] = 0x4B] = "callsuperid";
TMSA_OP_MAP[TMSA_OP_MAP["callproplex"] = 0x4C] = "callproplex";
TMSA_OP_MAP[TMSA_OP_MAP["callinterface"] = 0x4D] = "callinterface";
TMSA_OP_MAP[TMSA_OP_MAP["callsupervoid"] = 0x4E] = "callsupervoid";
TMSA_OP_MAP[TMSA_OP_MAP["callpropvoid"] = 0x4F] = "callpropvoid";
TMSA_OP_MAP[TMSA_OP_MAP["sxi1"] = 0x50] = "sxi1";
TMSA_OP_MAP[TMSA_OP_MAP["sxi8"] = 0x51] = "sxi8";
TMSA_OP_MAP[TMSA_OP_MAP["sxi16"] = 0x52] = "sxi16";
TMSA_OP_MAP[TMSA_OP_MAP["applytype"] = 0x53] = "applytype";
TMSA_OP_MAP[TMSA_OP_MAP["pushfloat4"] = 0x54] = "pushfloat4";
TMSA_OP_MAP[TMSA_OP_MAP["newobject"] = 0x55] = "newobject";
TMSA_OP_MAP[TMSA_OP_MAP["newarray"] = 0x56] = "newarray";
TMSA_OP_MAP[TMSA_OP_MAP["newactivation"] = 0x57] = "newactivation";
TMSA_OP_MAP[TMSA_OP_MAP["newclass"] = 0x58] = "newclass";
TMSA_OP_MAP[TMSA_OP_MAP["getdescendants"] = 0x59] = "getdescendants";
TMSA_OP_MAP[TMSA_OP_MAP["newcatch"] = 0x5A] = "newcatch";
TMSA_OP_MAP[TMSA_OP_MAP["findpropstrict"] = 0x5D] = "findpropstrict";
TMSA_OP_MAP[TMSA_OP_MAP["findproperty"] = 0x5E] = "findproperty";
TMSA_OP_MAP[TMSA_OP_MAP["finddef"] = 0x5F] = "finddef";
TMSA_OP_MAP[TMSA_OP_MAP["getlex"] = 0x60] = "getlex";
TMSA_OP_MAP[TMSA_OP_MAP["setproperty"] = 0x61] = "setproperty";
TMSA_OP_MAP[TMSA_OP_MAP["getlocal"] = 0x62] = "getlocal";
TMSA_OP_MAP[TMSA_OP_MAP["setlocal"] = 0x63] = "setlocal";
TMSA_OP_MAP[TMSA_OP_MAP["getglobalscope"] = 0x64] = "getglobalscope";
TMSA_OP_MAP[TMSA_OP_MAP["getscopeobject"] = 0x65] = "getscopeobject";
TMSA_OP_MAP[TMSA_OP_MAP["getproperty"] = 0x66] = "getproperty";
TMSA_OP_MAP[TMSA_OP_MAP["getouterscope"] = 0x67] = "getouterscope";
TMSA_OP_MAP[TMSA_OP_MAP["initproperty"] = 0x68] = "initproperty";
TMSA_OP_MAP[TMSA_OP_MAP["setpropertylate"] = 0x69] = "setpropertylate";
TMSA_OP_MAP[TMSA_OP_MAP["deleteproperty"] = 0x6A] = "deleteproperty";
TMSA_OP_MAP[TMSA_OP_MAP["deletepropertylate"] = 0x6B] = "deletepropertylate";
TMSA_OP_MAP[TMSA_OP_MAP["getslot"] = 0x6C] = "getslot";
TMSA_OP_MAP[TMSA_OP_MAP["setslot"] = 0x6D] = "setslot";
TMSA_OP_MAP[TMSA_OP_MAP["getglobalslot"] = 0x6E] = "getglobalslot";
TMSA_OP_MAP[TMSA_OP_MAP["setglobalslot"] = 0x6F] = "setglobalslot";
TMSA_OP_MAP[TMSA_OP_MAP["convert_s"] = 0x70] = "convert_s";
TMSA_OP_MAP[TMSA_OP_MAP["esc_xelem"] = 0x71] = "esc_xelem";
TMSA_OP_MAP[TMSA_OP_MAP["esc_xattr"] = 0x72] = "esc_xattr";
TMSA_OP_MAP[TMSA_OP_MAP["convert_i"] = 0x73] = "convert_i";
TMSA_OP_MAP[TMSA_OP_MAP["convert_u"] = 0x74] = "convert_u";
TMSA_OP_MAP[TMSA_OP_MAP["convert_d"] = 0x75] = "convert_d";
TMSA_OP_MAP[TMSA_OP_MAP["convert_b"] = 0x76] = "convert_b";
TMSA_OP_MAP[TMSA_OP_MAP["convert_o"] = 0x77] = "convert_o";
TMSA_OP_MAP[TMSA_OP_MAP["checkfilter"] = 0x78] = "checkfilter";
TMSA_OP_MAP[TMSA_OP_MAP["convert_f"] = 0x79] = "convert_f";
TMSA_OP_MAP[TMSA_OP_MAP["unplus"] = 0x7a] = "unplus";
TMSA_OP_MAP[TMSA_OP_MAP["convert_f4"] = 0x7b] = "convert_f4";
TMSA_OP_MAP[TMSA_OP_MAP["coerce"] = 0x80] = "coerce";
TMSA_OP_MAP[TMSA_OP_MAP["coerce_b"] = 0x81] = "coerce_b";
TMSA_OP_MAP[TMSA_OP_MAP["coerce_a"] = 0x82] = "coerce_a";
TMSA_OP_MAP[TMSA_OP_MAP["coerce_i"] = 0x83] = "coerce_i";
TMSA_OP_MAP[TMSA_OP_MAP["coerce_d"] = 0x84] = "coerce_d";
TMSA_OP_MAP[TMSA_OP_MAP["coerce_s"] = 0x85] = "coerce_s";
TMSA_OP_MAP[TMSA_OP_MAP["astype"] = 0x86] = "astype";
TMSA_OP_MAP[TMSA_OP_MAP["astypelate"] = 0x87] = "astypelate";
TMSA_OP_MAP[TMSA_OP_MAP["coerce_u"] = 0x88] = "coerce_u";
TMSA_OP_MAP[TMSA_OP_MAP["coerce_o"] = 0x89] = "coerce_o";
TMSA_OP_MAP[TMSA_OP_MAP["negate"] = 0x90] = "negate";
TMSA_OP_MAP[TMSA_OP_MAP["increment"] = 0x91] = "increment";
TMSA_OP_MAP[TMSA_OP_MAP["inclocal"] = 0x92] = "inclocal";
TMSA_OP_MAP[TMSA_OP_MAP["decrement"] = 0x93] = "decrement";
TMSA_OP_MAP[TMSA_OP_MAP["declocal"] = 0x94] = "declocal";
TMSA_OP_MAP[TMSA_OP_MAP["typeof"] = 0x95] = "typeof";
TMSA_OP_MAP[TMSA_OP_MAP["not"] = 0x96] = "not";
TMSA_OP_MAP[TMSA_OP_MAP["bitnot"] = 0x97] = "bitnot";
TMSA_OP_MAP[TMSA_OP_MAP["add"] = 0xA0] = "add";
TMSA_OP_MAP[TMSA_OP_MAP["subtract"] = 0xA1] = "subtract";
TMSA_OP_MAP[TMSA_OP_MAP["multiply"] = 0xA2] = "multiply";
TMSA_OP_MAP[TMSA_OP_MAP["divide"] = 0xA3] = "divide";
TMSA_OP_MAP[TMSA_OP_MAP["modulo"] = 0xA4] = "modulo";
TMSA_OP_MAP[TMSA_OP_MAP["lshift"] = 0xA5] = "lshift";
TMSA_OP_MAP[TMSA_OP_MAP["rshift"] = 0xA6] = "rshift";
TMSA_OP_MAP[TMSA_OP_MAP["urshift"] = 0xA7] = "urshift";
TMSA_OP_MAP[TMSA_OP_MAP["bitand"] = 0xA8] = "bitand";
TMSA_OP_MAP[TMSA_OP_MAP["bitor"] = 0xA9] = "bitor";
TMSA_OP_MAP[TMSA_OP_MAP["bitxor"] = 0xAA] = "bitxor";
TMSA_OP_MAP[TMSA_OP_MAP["equals"] = 0xAB] = "equals";
TMSA_OP_MAP[TMSA_OP_MAP["strictequals"] = 0xAC] = "strictequals";
TMSA_OP_MAP[TMSA_OP_MAP["lessthan"] = 0xAD] = "lessthan";
TMSA_OP_MAP[TMSA_OP_MAP["lessequals"] = 0xAE] = "lessequals";
TMSA_OP_MAP[TMSA_OP_MAP["greaterthan"] = 0xAF] = "greaterthan";
TMSA_OP_MAP[TMSA_OP_MAP["greaterequals"] = 0xB0] = "greaterequals";
TMSA_OP_MAP[TMSA_OP_MAP["instanceof"] = 0xB1] = "instanceof";
TMSA_OP_MAP[TMSA_OP_MAP["istype"] = 0xB2] = "istype";
TMSA_OP_MAP[TMSA_OP_MAP["istypelate"] = 0xB3] = "istypelate";
TMSA_OP_MAP[TMSA_OP_MAP["in"] = 0xB4] = "in";
TMSA_OP_MAP[TMSA_OP_MAP["increment_i"] = 0xC0] = "increment_i";
TMSA_OP_MAP[TMSA_OP_MAP["decrement_i"] = 0xC1] = "decrement_i";
TMSA_OP_MAP[TMSA_OP_MAP["inclocal_i"] = 0xC2] = "inclocal_i";
TMSA_OP_MAP[TMSA_OP_MAP["declocal_i"] = 0xC3] = "declocal_i";
TMSA_OP_MAP[TMSA_OP_MAP["negate_i"] = 0xC4] = "negate_i";
TMSA_OP_MAP[TMSA_OP_MAP["add_i"] = 0xC5] = "add_i";
TMSA_OP_MAP[TMSA_OP_MAP["subtract_i"] = 0xC6] = "subtract_i";
TMSA_OP_MAP[TMSA_OP_MAP["multiply_i"] = 0xC7] = "multiply_i";
TMSA_OP_MAP[TMSA_OP_MAP["getlocal0"] = 0xD0] = "getlocal0";
TMSA_OP_MAP[TMSA_OP_MAP["getlocal1"] = 0xD1] = "getlocal1";
TMSA_OP_MAP[TMSA_OP_MAP["getlocal2"] = 0xD2] = "getlocal2";
TMSA_OP_MAP[TMSA_OP_MAP["getlocal3"] = 0xD3] = "getlocal3";
TMSA_OP_MAP[TMSA_OP_MAP["setlocal0"] = 0xD4] = "setlocal0";
TMSA_OP_MAP[TMSA_OP_MAP["setlocal1"] = 0xD5] = "setlocal1";
TMSA_OP_MAP[TMSA_OP_MAP["setlocal2"] = 0xD6] = "setlocal2";
TMSA_OP_MAP[TMSA_OP_MAP["setlocal3"] = 0xD7] = "setlocal3";
TMSA_OP_MAP[TMSA_OP_MAP["invalid"] = 0xED] = "invalid";
TMSA_OP_MAP[TMSA_OP_MAP["debug"] = 0xEF] = "debug";
TMSA_OP_MAP[TMSA_OP_MAP["debugline"] = 0xF0] = "debugline";
TMSA_OP_MAP[TMSA_OP_MAP["debugfile"] = 0xF1] = "debugfile";
TMSA_OP_MAP[TMSA_OP_MAP["bkptline"] = 0xF2] = "bkptline";
TMSA_OP_MAP[TMSA_OP_MAP["timestamp"] = 0xF3] = "timestamp";