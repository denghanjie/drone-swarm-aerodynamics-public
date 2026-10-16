const fs=require('fs'),path=require('path'),crypto=require('crypto');const {chromium}=require('playwright');
(async()=>{const out=path.resolve(process.argv[2]);fs.mkdirSync(out,{recursive:true});const b=await chromium.launch({executablePath:process.env.RESEARCH_CHROME,headless:true});try{
 const p=await b.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});await p.goto('http://127.0.0.1:8876/research/m31-source-reference-admission-2026-10-16/viewer/',{waitUntil:'networkidle'});await p.waitForFunction(()=>document.body.dataset.binding==='verified'&&!document.getElementById('reset').disabled);
 const shots=[];async function shot(name,target){const bytes=await(target||p).screenshot({path:path.join(out,name)});shots.push({path:name,bytes:bytes.length,sha256:crypto.createHash('sha256').update(bytes).digest('hex')});}
 if(!(await p.locator('.lead').innerText()).includes('normalized center speeds'))throw Error('Final normalization wording missing');
 await shot('desktop.png');await p.locator('#scene').scrollIntoViewIfNeeded();await shot('desktop-scene.png',p.locator('#scene'));await p.check('#overlay');await shot('overlay-scene.png',p.locator('#scene'));
 await p.setViewportSize({width:390,height:844});await p.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));await p.uncheck('#overlay');await p.locator('#scene').scrollIntoViewIfNeeded();await shot('mobile-scene.png',p.locator('#scene'));
 fs.writeFileSync(path.join(out,'capture.json'),JSON.stringify({kind:'final-text-and-visual-capture',newScientificCalculation:false,fullQARerun:false,normalizationWordingChecked:true,screenshots:shots},null,2)+'\n');
}finally{await b.close();}})().catch(e=>{console.error(e.message);process.exitCode=1;});
