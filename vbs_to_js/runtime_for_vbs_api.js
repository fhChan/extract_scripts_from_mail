function left(str, lngLen) {
    if (lngLen > 0) {
        return str.substring(0, lngLen)
    } else {
        return null
    }
}
function right(str, lngLen) {
    if (str.length - lngLen >= 0 && str.length >= 0 && str.length - lngLen <= str.length) {
        return str.substring(str.length - lngLen, str.length)
    } else {
        return null
    }
}
function mid(str, starnum, endnum) {
    if (str.length >= 0) {
        return str.substr(starnum, endnum)
    } else {
        return null
    }
}
function asc(str){
    return str.charCodeAt(0)
}
function ascb(str){
    return str.charCodeAt(0)
}
function getref(func){
    return eval(func)
}