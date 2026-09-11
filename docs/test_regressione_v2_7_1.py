import asyncio, subprocess, time, sys, re, json
from playwright.async_api import async_playwright
T=open('/mnt/user-data/uploads/TEST_ASTA_4_UPDATE.txt',encoding='utf-8').read()
B=re.findall(r"==================== UPDATE \d.*?====================\n(.*?)\n\nCHECK", T, re.S)
srv=subprocess.Popen(["python3","-m","http.server","8792"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
DROP={"ts","at","updatedAt","time","upd","when","t0","date","iso"}
def normal(o):
    if isinstance(o,dict): return {k:normal(v) for k,v in sorted(o.items()) if k not in DROP}
    if isinstance(o,list): return [normal(x) for x in o]
    if isinstance(o,str) and re.search(r"\d{1,2}[:.]\d{2}", o): return re.sub(r"\d{1,2}[:.]\d{2}(:\d{2})?","HH:MM",o)
    return o
async def imp(pg, block):
    await pg.click("button[data-tab='importa']"); await pg.fill("textarea", block.strip())
    await pg.get_by_role("button", name=re.compile(r"^Leggi")).first.click()
    await pg.get_by_role("button", name=re.compile(r"^Applica")).first.click(); await pg.wait_for_timeout(120)
async def register(pg, name, price, choice):
    await pg.click("button[data-tab='cerca']"); await pg.fill("#q", name); await pg.wait_for_timeout(120)
    await pg.click(f"button[data-open='{name}']"); await pg.wait_for_timeout(120)
    if price is not None: await pg.fill("#price", str(price))
    await pg.click(f"label.outcome-choice:has(input[value='{choice}'])")
    await pg.click("button[data-outcome]"); await pg.wait_for_timeout(150)
    return await pg.input_value("#q")
async def run(file, vp):
    out={"file":file,"checks":{}}
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport=vp, has_touch=True); pg=await ctx.new_page()
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
        await pg.goto(f"http://localhost:8792/{file}"); await pg.wait_for_timeout(900)
        c=out["checks"]
        await imp(pg,B[0]); await imp(pg,B[1])
        # 1 ricerca live: suggerimenti visibili digitando
        await pg.click("button[data-tab='cerca']"); await pg.fill("#q","Sv"); await pg.wait_for_timeout(120)
        c["1_suggerimenti_live"]= await pg.locator("button[data-open]").count()>0
        # 2-3 scartato resta libero, ritorno ricerca vuota
        c["2_ritorno_ricerca_vuota"]= (await register(pg,"Orsolini",None,"__SCARTATO__"))==""
        await pg.fill("#q","Orsolini"); await pg.wait_for_timeout(120); await pg.click("button[data-open='Orsolini']")
        c["3_scartato_ripescabile"]= await pg.locator("button[data-outcome]").count()==1
        # UI: layout scheda (solo P1): OK visibile, etichetta prezzo non sovrapposta, trio sopra la piega
        ok=await pg.locator("button[data-outcome]").bounding_box(); H=vp["height"]
        c["ui_ok_raggiungibile_senza_scroll"]= ok is not None and ok["y"]+ok["height"]<=H
        trio=pg.locator(".price-trio"); c["ui_tre_numeri_sopra_piega"]= (await trio.count()==0) or ((await trio.bounding_box())["y"]<H)
        sm=pg.locator(".verdict .price small")
        if await sm.count():
            bs=await sm.bounding_box(); pr=await pg.locator(".verdict .price").bounding_box()
            c["ui_label_prezzo_non_sovrapposta"]= bs["y"]+bs["height"] <= pr["y"]+pr["height"]*0.45
        # prezzo mancante -> alert
        await register(pg,"Zaccagni",None,"Fight Club")
        c["4_alert_prezzo_mancante"]= "prezzi" in (await pg.inner_text("#topbar"))
        await register(pg,"Kean",40,"__PINTA__")
        # undo ultima azione
        await register(pg,"Scamacca",12,"NewRock")
        await pg.click("button[data-undolast]"); await pg.wait_for_timeout(150)
        await imp(pg,B[2]); await imp(pg,B[3])
        await imp(pg,"Zaccagni;Fight Club;9")
        c["5_alert_scompare_con_prezzo"]= "prezzi" not in (await pg.inner_text("#topbar"))
        # tabs render + rivali espansione
        for t in ["rosa","rivali","obiettivi","importa","impostazioni"]:
            await pg.click(f"button[data-tab='{t}']"); await pg.wait_for_timeout(120)
        await pg.click("button[data-tab='rivali']"); await pg.click(".rival-card.clickable >> nth=0"); await pg.wait_for_timeout(120)
        c["9_rivale_espande"]= await pg.locator(".rival-card.open").count()==1
        c["ui_header_altezza_px"]= round((await pg.locator("header.top").bounding_box())["height"])
        keys=await pg.evaluate("Object.keys(localStorage)")
        k=[x for x in keys if "state" in x.lower()]
        st=json.loads(await pg.evaluate(f"localStorage.getItem({json.dumps(k[0])})")) if k else None
        out["lskey"]=k; out["state"]=normal(st) if st else None
        c["pinta"]=[ (x["n"],x.get("p")) for x in st.get("mine",[])] if st else None
        c["asg_sample"]={n:st["asg"].get(n) for n in ["Svilar","Calhanoglu","Mancini","Dybala","Pulisic","Malen","Hojlund","Orsolini","Zaccagni","Scamacca"]} if st else None
        out["channel"]=await pg.evaluate("({beta:IS_BETA, ls:LS_STATE, branch:(typeof githubBranch==='function'?githubBranch():null), ver:APP_VERSION})")
        exp={"Svilar":["AS Emazz",25],"Calhanoglu":["Fight Club",84],"Mancini":["Space Invaders",31],"Dybala":["Big Tasty FC",52],"Pulisic":["AC OMMODITY",45],"Malen":["Fc Afragolese",65],"Hojlund":["Al-Chaos-Ahli",92],"Martinez L.":["S.S. Longobarda",105],"Thuram":["Fight Club",72],"Orsolini":["Fun Cool FC",28],"Zaccagni":["Fight Club",9]}
        bad={}
        for n,(t,pp) in exp.items():
            a=st["asg"].get(n) or {}
            if a.get("t")!=t or a.get("p")!=pp: bad[n]=a
        c["CHECK_file_test_assegnati"]= "PASS" if not bad else bad
        rem=st["set"]["budget"]-sum(int(x.get("p") or 0) for x in st["mine"])
        c["CHECK_crediti_AS_Pinta_(atteso_195=235-40_Kean)"]=rem
        c["CHECK_scamacca_annullato"]= "Scamacca" not in st["asg"]
        out["errors"]=errs
        await b.close()
    return out
async def main():
    vps={"ipadL":{"width":1180,"height":820},"iphone":{"width":390,"height":844}}
    res={}
    for f in sys.argv[1:]:
        for vn,vp in vps.items():
            res[f"{f}|{vn}"]=await run(f,vp)
    json.dump(res,open("regress_out.json","w"),ensure_ascii=False,indent=1)
    for k,v in res.items():
        print("==",k,"errori:",v["errors"],"lskey:",v["lskey"])
        for ck,cv in v["checks"].items():
            if ck not in ("pinta","asg_sample"): print("  ",ck,cv)
    base=[v for k,v in res.items() if k.startswith(sys.argv[1])]; new=[v for k,v in res.items() if k.startswith(sys.argv[2])]
    for a,b2 in zip(base,new):
        print("STATO IDENTICO ->", a["state"]==b2["state"], "| canale:", b2.get("channel"))
        def flat(o,pre=""):
            if isinstance(o,dict):
                r={}
                for k,v in o.items(): r.update(flat(v,pre+"/"+k))
                return r
            if isinstance(o,list): return {pre: json.dumps(o,ensure_ascii=False,sort_keys=True)}
            return {pre:o}
        fa,fb=flat(a["state"]),flat(b2["state"])
        print("  chiavi di stato diverse:", [k for k in sorted(set(fa)|set(fb)) if fa.get(k)!=fb.get(k)])
    print("pinta:", new[0]["checks"]["pinta"]); print("asg:", json.dumps(new[0]["checks"]["asg_sample"],ensure_ascii=False))
try: asyncio.run(main())
finally: srv.terminate()
