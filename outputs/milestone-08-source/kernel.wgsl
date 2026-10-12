struct State { p:vec4f, v:vec4f, q:vec4f, w:vec4f, f:vec4f }
struct Params { count:u32, steps:u32, dt:f32, pad:u32 }
@group(0) @binding(0) var<storage,read> input:array<State>;
@group(0) @binding(1) var<storage,read> commands:array<vec4f>;
@group(0) @binding(2) var<storage,read_write> output:array<State>;
@group(0) @binding(3) var<uniform> params:Params;
fn add(a:State,b:State,h:f32)->State {return State(a.p+h*b.p,a.v+h*b.v,a.q+h*b.q,a.w+h*b.w,a.f+h*b.f);}
fn deriv(s:State,u:vec4f)->State {
 let inertia=vec3f(1.4e-5,1.4e-5,2.17e-5);
 let thrust=dot(s.f,vec4f(1));
 let torque=vec3f(.028*(s.f.x+s.f.y-s.f.z-s.f.w),.028*(-s.f.x+s.f.y+s.f.z-s.f.w),(7.94e-12/3.16e-10)*(s.f.x-s.f.y+s.f.z-s.f.w));
 let a=vec3f(0,0,thrust/.027);let t=2*cross(s.q.xyz,a);let force=a+s.q.w*t+cross(s.q.xyz,t);
 let dq=.5*vec4f(s.q.w*s.w.xyz+cross(s.q.xyz,s.w.xyz),-dot(s.q.xyz,s.w.xyz));
 let dw=(torque-cross(s.w.xyz,s.w.xyz*inertia))/inertia;
 return State(vec4f(s.v.xyz,0),vec4f(force-vec3f(0,0,9.81),0),dq,vec4f(dw,0),(u-s.f)/.04);
}
@compute @workgroup_size(64)
fn main(@builtin(global_invocation_id) id:vec3u){
 if(id.x>=params.count){return;}var s=input[id.x];let u=commands[id.x];let h=params.dt;
 for(var k=0u;k<params.steps;k++){let a=deriv(s,u);let b=deriv(add(s,a,h*.5),u);let c=deriv(add(s,b,h*.5),u);let d=deriv(add(s,c,h),u);s=add(add(add(add(s,a,h/6),b,h/3),c,h/3),d,h/6);s.q=normalize(s.q);}
 output[id.x]=s;
}
