'use strict';
const fs=require('fs'),path=require('path');
// Development archive includes a pinned sparse checkout. Published placement is
// repository-root/research/campaign-spatial-pruning, referring to pinned outputs.
const local=path.resolve(__dirname,'../snapshot');
const root=fs.existsSync(path.join(local,'outputs/step02c-source/physics.cjs'))?local:path.resolve(__dirname,'../../..');
function source(relative){return require(path.join(root,relative));}
module.exports={source,root};
