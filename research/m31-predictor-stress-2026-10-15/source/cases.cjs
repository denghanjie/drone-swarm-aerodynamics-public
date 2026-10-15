'use strict';
// Fixed analytic inputs derived before field evaluation; no solver/model imports.
const weight=.027*9.81,pi=Math.PI;
const state=(p,v=[0,0,0],q=[0,0,0,1],omega=[0,0,0])=>[...p,...v,...q,...omega,...Array(4).fill(weight/4)];
const ids=['support-transit','cold-start-inflow','smooth-fast-reversal','fixed-position-source-pitch','two-source-receiver-roll','stacked-moving-sources'];
const descriptions={
 'support-transit':'Receiver crosses both finite radial wake edges and the core.',
 'cold-start-inflow':'Receiver starts inside the wake with nonzero lateral speed and no earlier samples.',
 'smooth-fast-reversal':'Two smooth lateral cycles with three interior direction reversals.',
 'fixed-position-source-pitch':'Stationary centers; source pitch swings between -15 and +15 degrees.',
 'two-source-receiver-roll':'Moving, rolling receiver encounters two overlapping source wakes.',
 'stacked-moving-sources':'Moving receiver below three sources, two moving; source-source fields retained.'
};
const reportingWindows={
 'cold-start-inflow':[{label:'startup 0–5 ms',startTick:0,endTick:20},{label:'second interval 5–10 ms',startTick:20,endTick:40}],
 'smooth-fast-reversal':[1000,2000,3000].map(t=>({label:`reversal at ${t*.00025}s ±10ms`,startTick:t-40,endTick:t+40}))
};
function poses(id,t){const p2=2*pi*t,p4=4*pi*t;
 switch(id){
 case 'support-transit':return [state([-.36+.72*t,.035,1],[.72,0,0]),state([0,0,1.8])];
 case 'cold-start-inflow':return [state([.14-.50*t,.035,1],[-.50,0,0]),state([0,0,1.8])];
 case 'smooth-fast-reversal':return [state([.12+.09*Math.cos(p4),.04,1],[-.36*pi*Math.sin(p4),0,0]),state([0,0,1.8])];
 case 'fixed-position-source-pitch':{const theta=pi/12*Math.sin(p4);return [state([.12,.035,1]),state([0,0,1.8],[0,0,0],[0,Math.sin(theta/2),0,Math.cos(theta/2)],[0,pi*pi/3*Math.cos(p4),0])];}
 case 'two-source-receiver-roll':{const beta=pi/18*Math.sin(p4);return [state([.1*Math.sin(p2),.035,1],[.2*pi*Math.cos(p2),0,0],[Math.sin(beta/2),0,0,Math.cos(beta/2)],[2*pi*pi/9*Math.cos(p4),0,0]),state([-.22,0,1.8]),state([.22,0,1.8])];}
 case 'stacked-moving-sources':return [state([.1*Math.sin(p2),.045*Math.cos(p2),1],[.2*pi*Math.cos(p2),-.09*pi*Math.sin(p2),0]),state([-.06,0,1.7]),state([.06+.08*Math.sin(p2),.02,2.1],[.16*pi*Math.cos(p2),0,0]),state([.04*Math.cos(p2),-.04,2.5],[-.08*pi*Math.sin(p2),0,0])];
 default:throw Error('Unknown prescribed case');
 }
}
module.exports={ids,descriptions,reportingWindows,poses};
