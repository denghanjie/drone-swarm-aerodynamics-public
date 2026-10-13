'use strict';
const boxes=[];function box(id,min,max,kind='equipment'){boxes.push({id,min,max,kind});}
box('floor',[-60,-10,-.4],[42,10,0],'shell');box('ceiling',[-14,-10,10],[42,10,10.4],'shell');box('north-wall',[-14,10,0],[42,10.4,10],'shell');box('south-wall',[-14,-10.4,0],[42,-10,10],'shell');
const gates=[{x:0,y:-2,z:4,width:5,height:4},{x:12,y:2,z:5.8,width:5,height:4},{x:24,y:-1,z:3.2,width:5,height:4}];
for(const [i,g] of gates.entries()){const y0=g.y-g.width/2,y1=g.y+g.width/2,z0=g.z-g.height/2,z1=g.z+g.height/2;box('partition-'+i+'-left',[g.x-.18,-10,0],[g.x+.18,y0,10],'partition');box('partition-'+i+'-right',[g.x-.18,y1,0],[g.x+.18,10,10],'partition');box('partition-'+i+'-below',[g.x-.18,y0,0],[g.x+.18,y1,z0],'partition');box('partition-'+i+'-above',[g.x-.18,y0,z1],[g.x+.18,y1,10],'partition');}
for(const x of [3.5,7,15.5,19,27.5,31])for(const side of [-1,1]){const y=side*7;box('rack-'+x+'-'+side,[x-.6,y-1.2,0],[x+.6,y+1.2,7],'rack');}
box('press-A',[4,-.2,0],[6,2.5,4.5]);box('press-B',[16,-4.8,0],[18,-1.8,6]);box('press-C',[28,1.5,0],[30,4.5,5.5]);
box('overhead-A',[6,-5,7.8],[9,5,8.4],'overhead');box('overhead-B',[18,-5,8.3],[21,5,8.9],'overhead');box('loading-platform',[32,-5,0],[34,0,1.2]);
const route=[[-7,-2,4],[1,-2,4],[6,-2.5,5.7],[10,2,5.8],[13,2,5.8],[18,2.5,5.8],[22,-1,3.2],[25,-1,3.2],[30,-1,3.7],[36,0,4]];
module.exports={id:'factory-v1',name:'Three factory halls',units:'metres',boxes,gates,route,finish:36,duration:120,description:'Synthetic factory: thick offset partitions, changing-height doorways, racks, presses and overhead structures. All shown solid boxes are checked. The ceiling and side shell can be visually hidden; their collisions remain active.'};
