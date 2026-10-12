
// Uncertainty-margin candidate: larger gate/lane clearance, lower position gain, later release. Fixed before holdout testing; no safety guarantee. No aerodynamic forces or position teleportation.
class Scheduler{
 constructor({width,spacing,speed,initial}){this.width=width;this.spacing=spacing;this.speed=speed;this.initial=initial;this.capacity=Math.min(5,Math.floor((width-.35)/.42)+1);this.row=0;this.phase=initial.map(()=> 'waiting');this.lanes=initial.map(p=>p[1]);this.active=[];this.events=[];}
 update(states,t){
  for(const i of this.active){const s=states[i];if(this.phase[i]==='stage'&&s[0]>-.61){this.phase[i]='align';this.events.push({t,id:i,phase:'align'});}if(this.phase[i]==='align'&&Math.abs(s[1]-this.lanes[i])<.02&&Math.abs(s[4])<.06&&Math.abs(s[0]+.45)<.05&&Math.abs(s[3])<.06){this.phase[i]='cross';this.events.push({t,id:i,phase:'cross'});}if(this.phase[i]==='cross'&&s[0]>.65){this.phase[i]='departed';this.events.push({t,id:i,phase:'departed'});}}
  if(this.active.length&&this.active.every(i=>this.phase[i]==='departed'))this.active=[];
  if(this.active.length)return;
  while(this.row<Math.ceil(states.length/5)&&this.phase.slice(this.row*5,this.row*5+5).every(p=>p==='departed')){this.row++;this.events.push({t,phase:'advance-row',row:this.row});}
  const ready=[];for(let i=this.row*5;i<Math.min(states.length,this.row*5+5);i++)if(this.phase[i]==='waiting')ready.push(i);
  if(!ready.length)return;
  // Wait until this front row has approached the staging line before reserving a batch.
  if(ready.some(i=>Math.abs(states[i][0]+1.2)>.035||Math.abs(states[i][3])>.06))return;
  this.active=ready.slice(0,this.capacity);const step=Math.min(this.spacing,(this.width-.35)/Math.max(1,this.active.length-1));
  this.active.forEach((i,j)=>{this.lanes[i]=(j-(this.active.length-1)/2)*step;this.phase[i]='stage';this.events.push({t,id:i,phase:'stage',lane:this.lanes[i]});});
 }
 command(i,s){const p=this.phase[i];let tx,ty,vx;if(p==='waiting'){tx=-1.2-(Math.floor(i/5)-this.row)*this.spacing;ty=this.initial[i][1];vx=.8*(tx-s[0]);}else if(p==='stage'){tx=-.45;ty=this.initial[i][1];vx=.8*(tx-s[0]);}else if(p==='align'){tx=-.45;ty=this.lanes[i];vx=.8*(tx-s[0]);}else{ty=this.lanes[i];vx=this.speed;}
  return {vx,vy:.8*(ty-s[1]),refY:ty};
 }
}
export {Scheduler};
