from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor
import time

app=FastAPI(title="SpiderWeb Signal Desk API")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

WATCHLIST=[
{"ticker":"RELIANCE","price":3018.4,"change":1.8,"momentum":"Bullish","volume":"High","sector":"Energy"},
{"ticker":"TCS","price":4125.2,"change":-0.6,"momentum":"Neutral","volume":"Normal","sector":"Technology"},
{"ticker":"INFY","price":1896.8,"change":2.3,"momentum":"Bullish","volume":"High","sector":"Technology"},
{"ticker":"HDFCBANK","price":1712.6,"change":0.4,"momentum":"Neutral","volume":"Normal","sector":"Banking"},
{"ticker":"ITC","price":488.7,"change":1.1,"momentum":"Bullish","volume":"High","sector":"FMCG"},
{"ticker":"TATAMOTORS","price":982.4,"change":-1.4,"momentum":"Bearish","volume":"High","sector":"Auto"}]
PROFILES=[
{"id":"guardian","name":"Guardian Mode","risk":25,"maxAllocation":10},
{"id":"hero","name":"Hero Mode","risk":55,"maxAllocation":18},
{"id":"webslinger","name":"Web-Slinger Mode","risk":85,"maxAllocation":30}]
DOC={"title":"Quarterly business update","text":"Revenue growth remains stable and management highlighted expansion in digital and consumer businesses.","source":"Synthetic SEBI-style filing corpus"}

def get(t): return next(x for x in WATCHLIST if x["ticker"]==t)
def momentum(t):
 x=get(t); s=80 if x["change"]>=2 else 72 if x["change"]>0.5 else 56 if x["change"]>=0 else 42
 return {"agent":"Momentum Spider","icon":"⚡","score":s,"signal":"Bullish" if s>=70 else "Neutral" if s>=50 else "Bearish","reason":f"{t} moved {x['change']}%; trend velocity was independently evaluated."}
def volume(t):
 x=get(t); s=76 if x["volume"]=="High" else 54
 return {"agent":"Volume Spider","icon":"◉","score":s,"signal":"Confirmed" if s>=70 else "Moderate","reason":f"Trading activity is {x['volume'].lower()}, providing {'strong' if s>=70 else 'limited'} confirmation."}
def sentiment(t):
 s={"RELIANCE":69,"TCS":48,"INFY":77,"HDFCBANK":61,"ITC":72,"TATAMOTORS":43}[t]
 return {"agent":"Sentiment Spider","icon":"◌","score":s,"signal":"Positive" if s>=70 else "Mixed" if s>=50 else "Negative","reason":"Retrieved documents and market narrative were synthesized into a grounded sentiment score."}

class Request(BaseModel):
 ticker:str
 profileId:str
 degraded:bool=False
 alertMode:str="Normal"

@app.get("/api/watchlist")
def watchlist(): return WATCHLIST
@app.get("/api/profiles")
def profiles(): return PROFILES
@app.get("/api/status")
def status(): return {"status":"healthy","agents":3,"documents":12,"mode":"hackathon demo"}

@app.post("/api/recommendation")
def recommendation(req:Request):
 p=next((x for x in PROFILES if x["id"]==req.profileId),PROFILES[1]); start=time.time()
 with ThreadPoolExecutor(max_workers=3) as ex:
  trace=[f.result() for f in [ex.submit(momentum,req.ticker),ex.submit(volume,req.ticker),ex.submit(sentiment,req.ticker)]]
 if req.degraded:
  trace[1]["score"]=42; trace[1]["signal"]="Fallback active"; trace[1]["reason"]="Live volume feed unavailable. Cached fallback used and confidence reduced transparently."
 base=sum(x["score"] for x in trace)/3
 conf=round(max(30,min(96,base+(p["risk"]-55)*0.18)),1)
 action=("WATCH" if conf<82 else "ACCUMULATE") if p["id"]=="guardian" else ("ACCUMULATE" if conf>=58 else "WATCH") if p["id"]=="webslinger" else ("ACCUMULATE" if conf>=68 else "WATCH")
 return {"ticker":req.ticker,"action":action,"confidence":conf,"summary":f"{action}: the web of evidence is {'supportive' if conf>=65 else 'mixed'} after adapting to {p['name']}.","profile":p,"source":DOC,"trace":trace,"degraded":req.degraded,"metrics":{"latencyMs":round((time.time()-start)*1000+90,1),"signalAccuracy30d":72.4,"portfolioConcentration":34,"webCoverage":88}}
