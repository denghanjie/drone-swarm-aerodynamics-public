'use strict';
// Read-only PNG pixel comparison for browser screenshots; no image editing.
const zlib=require('node:zlib');
function decode(buffer){
 if(buffer.subarray(0,8).toString('hex')!=='89504e470d0a1a0a')throw Error('Not PNG');
 let width,height,bpp;const parts=[];
 for(let p=8;p<buffer.length;){const n=buffer.readUInt32BE(p),type=buffer.toString('ascii',p+4,p+8),d=buffer.subarray(p+8,p+8+n);if(type==='IHDR'){width=d.readUInt32BE(0);height=d.readUInt32BE(4);if(d[8]!==8||![2,6].includes(d[9])||d[12]!==0)throw Error('Unsupported PNG encoding');bpp=d[9]===6?4:3;}if(type==='IDAT')parts.push(d);p+=n+12;}
 const bytes=zlib.inflateSync(Buffer.concat(parts)),stride=width*bpp,pixels=Buffer.alloc(width*height*bpp);if(bytes.length!==height*(stride+1))throw Error('PNG size differs');
 const paeth=(a,b,c)=>{const p=a+b-c,pa=Math.abs(p-a),pb=Math.abs(p-b),pc=Math.abs(p-c);return pa<=pb&&pa<=pc?a:pb<=pc?b:c;};
 for(let y=0;y<height;y++){const filter=bytes[y*(stride+1)];if(filter>4)throw Error('PNG filter');for(let x=0;x<stride;x++){const at=y*stride+x,left=x>=bpp?pixels[at-bpp]:0,up=y?pixels[at-stride]:0,upperLeft=y&&x>=bpp?pixels[at-stride-bpp]:0,predictor=[0,left,up,Math.floor((left+up)/2),paeth(left,up,upperLeft)][filter];pixels[at]=(bytes[y*(stride+1)+1+x]+predictor)&255;}}
 return {width,height,bpp,pixels};
}
function compare(first,second,inset=0){
 const a=decode(first),b=decode(second);if(a.width!==b.width||a.height!==b.height||a.bpp!==b.bpp)throw Error('Screenshot dimensions differ');
 let changedPixels=0,maxChannelDifference=0,totalDifference=0,minX=a.width,minY=a.height,maxX=-1,maxY=-1,totalPixels=0;
 for(let y=inset;y<a.height-inset;y++)for(let x=inset;x<a.width-inset;x++){const p=(y*a.width+x)*a.bpp;let changed=false;totalPixels++;for(let k=0;k<a.bpp;k++){const d=Math.abs(a.pixels[p+k]-b.pixels[p+k]);changed ||= d!==0;maxChannelDifference=Math.max(maxChannelDifference,d);totalDifference+=d;}if(changed){changedPixels++;minX=Math.min(minX,x);minY=Math.min(minY,y);maxX=Math.max(maxX,x);maxY=Math.max(maxY,y);}}
 return {width:a.width,height:a.height,inset,totalPixels,changedPixels,changedFraction:changedPixels/totalPixels,maxChannelDifference,meanChannelDifference:totalDifference/(totalPixels*a.bpp),changedBounds:changedPixels?[minX,minY,maxX,maxY]:null};
}
module.exports={compare};
