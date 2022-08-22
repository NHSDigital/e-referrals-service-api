const proxy_path = context.getVariable('proxy.pathsuffix');
const regex = /.*\/Binary.*/;
const found = proxy_path.match(regex);

const is_binary_path = found ? true : false;

context.setVariable("isBinaryPath", is_binary_path);
