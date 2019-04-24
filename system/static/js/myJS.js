
function getXMLHttpRequest(){
    var xmlhttp;
        if(window.XMLHttpRequest){// code for IE7+,Firefox,chrome,opera,safari
            xmlhttp=new XMLHttpRequest();
        }else{// code for IE6,IE7
            xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
        }
        return xmlhttp;
}