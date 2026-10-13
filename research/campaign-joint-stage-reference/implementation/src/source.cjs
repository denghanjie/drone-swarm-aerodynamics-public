'use strict';
const path=require('path');
const root=path.resolve(__dirname,'../snapshot');
function source(relative){return require(path.join(root,relative));}
module.exports={source,root};
