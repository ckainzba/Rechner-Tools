import re
import os

filepath = '/Users/ckainzba/.gemini/antigravity-ide/scratch/rechner-tools/investment/haltedauerrechner/index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract script block exactly
script_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
script_code = script_match.group(1) if script_match else ""

# Ensure we have the logic
if not script_code:
    print("Error extracting script")
    exit(1)

new_html = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Haltedauer-Rechner – Rechner & Tools</title>
    <meta name="description" content="Wie lange muss ich investiert bleiben, um Verlustrisiken zu minimieren? Analyse historischer MSCI-World-Renditedaten.">
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;800&display=swap" rel="stylesheet">
    
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="data.js"></script>

    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            font-family: 'Roboto', sans-serif;
            background: #ffffff;
            color: #1e293b;
            min-height: 100vh;
            padding-bottom: 80px;
        }}
        
        .back-btn {{
            display: inline-flex; align-items: center; gap: 7px;
            font-size: 13.5px; font-weight: 500; color: #646464;
            text-decoration: none; padding: 6px 0; transition: color 0.15s;
        }}
        .back-btn:hover {{ color: #023e84; }}
        .back-btn svg {{ width: 16px; height: 16px; stroke: currentColor; fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; transition: transform 0.15s; }}
        .back-btn:hover svg {{ transform: translateX(-2px); }}

        .badge-brand {{
            display: inline-block; padding: 4px 14px; border-radius: 20px;
            background: rgba(0, 111, 185, 0.08); border: 1px solid rgba(0, 111, 185, 0.2);
            color: #006fb9; font-size: 0.73rem; font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 14px;
        }}

        .card-panel {{
            background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.03); transition: box-shadow 0.2s, border-color 0.2s;
        }}
        .card-panel:hover {{ box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06); }}

        .result-card {{
            background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
            padding: 22px 20px; box-shadow: 0 4px 18px rgba(0, 0, 0, 0.03);
            transition: all 0.2s;
        }}
        .result-card:hover {{ border-color: #cbd5e1; transform: translateY(-2px); box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06); }}

        .icon-box {{
            width: 42px; height: 42px; border-radius: 12px; background: #e8f0fa; color: #023e84;
            display: flex; align-items: center; justify-content: center; margin-bottom: 16px;
        }}

        /* Slider Styling */
        input[type=range] {{
            -webkit-appearance: none; appearance: none; width: 100%; height: 6px; border-radius: 3px;
            background: #e5e7eb; outline: none; cursor: pointer; transition: all 0.2s ease;
        }}
        input[type=range]::-webkit-slider-thumb {{
            -webkit-appearance: none; appearance: none; width: 20px; height: 20px; border-radius: 50%;
            background: #023e84; cursor: pointer; border: none; box-shadow: 0 2px 4px rgba(2, 62, 132, 0.25);
            transition: transform 0.15s ease;
        }}
        input[type=range]::-webkit-slider-thumb:hover {{ transform: scale(1.12); }}

        .qp-btn {{
            padding: 5px 14px; border-radius: 20px; border: 1px solid #e2e8f0; background: transparent;
            color: #64748b; font-size: 0.8rem; font-family: 'Inter', sans-serif; font-weight: 500; cursor: pointer; transition: all 0.15s;
        }}
        .qp-btn:hover, .qp-btn.active {{ border-color: #006fb9; color: #006fb9; background: rgba(0, 111, 185, 0.08); }}

        /* Rev Inputs */
        .rev-input {{
            background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 14px;
            color: #1e293b; font-weight: 700; width: 100px; outline: none; transition: border-color 0.15s;
        }}
        .rev-input:focus {{ border-color: #006fb9; }}

        .prob-fill {{ transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1); }}
        
        @keyframes fadeUp {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .animate-in {{ animation: fadeUp 0.28s ease forwards; }}

        /* Table Classes for JS */
        .td-pos {{ color: #047857; font-weight: 600; padding: 10px; border-bottom: 1px solid #e2e8f0; }}
        .td-neg {{ color: #9f1239; font-weight: 600; padding: 10px; border-bottom: 1px solid #e2e8f0; }}
        .td-period {{ color: #023e84; font-size: 0.85rem; padding: 10px; border-bottom: 1px solid #e2e8f0; font-weight: 500; }}
        
        details summary::-webkit-details-marker {{ display:none; }}
    </style>
</head>
<body>

    <div class="max-w-[1100px] mx-auto px-6 pt-8">
        <a href="../../index.html" class="back-btn mb-6" id="btn-back-home">
            <svg viewBox="0 0 24 24"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
            Zurück zur Übersicht
        </a>
    </div>

    <header class="text-center pb-8 pt-4">
        <div class="badge-brand">MSCI World &middot; 1925–2025</div>
        <h1 class="text-3xl md:text-4xl font-extrabold text-[#023e84] mb-3 tracking-tight">Haltedauer-Rechner</h1>
        <p class="text-slate-500 max-w-[540px] mx-auto leading-relaxed">
            Wie lange muss ich anlegen, um mit hoher Wahrscheinlichkeit eine bestimmte Rendite zu erzielen?
        </p>
    </header>

    <div class="max-w-[1100px] mx-auto px-6">
        
        <!-- Eingabe Panel -->
        <div class="card-panel p-6 md:p-8 mb-8">
            <div class="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-400 mb-6">
                <div class="w-6 h-6 rounded-md bg-[#023e84]/10 text-[#023e84] flex items-center justify-center">
                    <svg viewBox="0 0 24 24" class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="4" x2="20" y1="21" y2="21"/><line x1="4" x2="20" y1="14" y2="14"/><line x1="4" x2="20" y1="7" y2="7"/><polyline points="14 17 14 21 18 21"/><polyline points="8 10 8 14 12 14"/><polyline points="14 3 14 7 18 7"/></svg>
                </div>
                Eingabe & Filter
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-10">
                <!-- Haltedauer -->
                <div>
                    <div class="text-sm font-medium text-slate-500 mb-2">Gewünschte Haltedauer</div>
                    <div class="text-[2.8rem] font-extrabold text-[#006fb9] leading-none mb-4" id="yearDisplay">15 <span class="text-base font-normal text-slate-500 ml-1">Jahre</span></div>
                    <input type="range" id="slider" min="1" max="50" value="15">
                    <div class="flex justify-between mt-2 text-xs text-slate-400">
                        <span>1 J</span><span>10</span><span>20</span><span>30</span><span>40</span><span>50 J</span>
                    </div>
                    <div class="flex flex-wrap gap-2 mt-4">
                        <button class="qp-btn" onclick="setN(1)">1 J</button>
                        <button class="qp-btn" onclick="setN(3)">3 J</button>
                        <button class="qp-btn" onclick="setN(5)">5 J</button>
                        <button class="qp-btn" onclick="setN(10)">10 J</button>
                        <button class="qp-btn active" onclick="setN(15)">15 J</button>
                        <button class="qp-btn" onclick="setN(20)">20 J</button>
                        <button class="qp-btn" onclick="setN(30)">30 J</button>
                    </div>
                </div>

                <!-- Zielrendite -->
                <div>
                    <div class="text-sm font-medium text-slate-500 mb-2">Mindest-Zielrendite (optional)</div>
                    <div class="text-[2.8rem] font-extrabold text-[#006fb9] leading-none mb-4" id="targetReturnDisplay">3 <span class="text-base font-normal text-slate-500 ml-1">% p.a.</span></div>
                    <input type="hidden" id="targetReturn" value="3" />
                    <input type="range" id="sl-targetReturn" min="0" max="10" step="0.5" value="3">
                    <div class="flex justify-between mt-2 text-xs text-slate-400 mb-4">
                        <span>0 %</span><span>10 %</span>
                    </div>
                    <div class="text-[0.8rem] text-slate-500 leading-relaxed">
                        Wie wahrscheinlich ist es, über die gewählte Haltedauer <strong>mindestens diese Rendite</strong> zu erzielen? (0 % = Wahrscheinlichkeit auf Gewinn)
                    </div>
                </div>

                <!-- Auswertung Info -->
                <div>
                    <div class="text-sm font-medium text-slate-500 mb-2">Ausgewertete Perioden</div>
                    <div class="text-[2.8rem] font-extrabold text-[#023e84] leading-none mb-2" id="countValue">–</div>
                    <div class="text-sm text-slate-500" id="countSub">Zeitraum 1925–2025</div>
                </div>
            </div>
        </div>

        <!-- Result Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <div class="result-card">
                <div class="icon-box">
                    <svg viewBox="0 0 24 24" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 15.5 15.5"/></svg>
                </div>
                <div class="text-[0.72rem] font-semibold tracking-wider uppercase text-slate-500 mb-1">Wahrscheinlichkeit ≥ Zielrendite</div>
                <div class="text-3xl font-extrabold text-[#047857]" id="probValue">–</div>
                <div class="w-full h-1.5 bg-slate-100 rounded-full mt-3 overflow-hidden">
                    <div class="h-full bg-[#006fb9] prob-fill" id="probFill" style="width:0%"></div>
                </div>
                <div class="text-xs text-slate-500 mt-2" id="probSub"></div>
            </div>

            <div class="result-card">
                <div class="icon-box">
                    <svg viewBox="0 0 24 24" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 17 13.5 8.5 8.5 13.5 1 6"/><polyline points="16 17 22 17 22 11"/></svg>
                </div>
                <div class="text-[0.72rem] font-semibold tracking-wider uppercase text-slate-500 mb-1">Schlechteste Periode</div>
                <div class="text-3xl font-extrabold text-[#9f1239]" id="worstValue">–</div>
                <div class="text-xs text-slate-500 mt-2" id="worstSub"></div>
            </div>

            <div class="result-card">
                <div class="icon-box">
                    <svg viewBox="0 0 24 24" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 7 13.5 15.5 8.5 10.5 1 18"/><polyline points="16 7 22 7 22 13"/></svg>
                </div>
                <div class="text-[0.72rem] font-semibold tracking-wider uppercase text-slate-500 mb-1">Beste Periode</div>
                <div class="text-3xl font-extrabold text-[#047857]" id="bestValue">–</div>
                <div class="text-xs text-slate-500 mt-2" id="bestSub"></div>
            </div>

            <div class="result-card">
                <div class="icon-box">
                    <svg viewBox="0 0 24 24" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
                </div>
                <div class="text-[0.72rem] font-semibold tracking-wider uppercase text-slate-500 mb-1">Durchschnitt p.a.</div>
                <div class="text-3xl font-extrabold text-[#023e84]" id="avgValue">–</div>
                <div class="text-xs text-slate-500 mt-2" id="avgSub"></div>
            </div>
        </div>

        <!-- Table Panel -->
        <details class="card-panel mb-8 group cursor-pointer" id="periodsPanel">
            <summary class="p-6 flex justify-between items-center text-sm font-bold uppercase tracking-wider text-slate-500 hover:text-[#023e84] transition-colors">
                Beste & Schlechteste Perioden im Detail
                <svg viewBox="0 0 24 24" class="w-5 h-5 stroke-current fill-none stroke-2 transition-transform duration-300 group-open:rotate-180"><polyline points="6 9 12 15 18 9"/></svg>
            </summary>
            <div class="px-6 pb-6 border-t border-slate-100 mt-2 pt-4 overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr>
                            <th class="pb-3 text-xs font-semibold text-slate-400 uppercase border-b border-slate-200">Zeitraum</th>
                            <th class="pb-3 text-xs font-semibold text-slate-400 uppercase border-b border-slate-200">Rendite p.a.</th>
                            <th class="pb-3 text-xs font-semibold text-slate-400 uppercase border-b border-slate-200">Dauer</th>
                        </tr>
                    </thead>
                    <tbody id="periodsBody"></tbody>
                </table>
            </div>
        </details>

        <!-- Reverse Calculator -->
        <div class="card-panel p-6 md:p-8 mb-12 bg-slate-50/50">
            <div class="flex items-center gap-3 mb-2">
                <div class="w-8 h-8 rounded-full bg-white shadow-sm flex items-center justify-center text-xl">⏱</div>
                <h2 class="text-lg font-bold text-slate-800">Wie lange MUSS ich anlegen?</h2>
            </div>
            <p class="text-sm text-slate-500 mb-6 max-w-2xl">Gib die gewünschte Zielrendite und die Mindestwahrscheinlichkeit ein – der Rechner ermittelt basierend auf den historischen Daten die kürzeste notwendige Haltedauer.</p>
            
            <div class="flex flex-wrap items-end gap-6 mb-6">
                <div>
                    <label class="block text-xs font-bold uppercase tracking-wide text-slate-500 mb-2">Zielrendite p.a.</label>
                    <div class="flex items-center gap-2">
                        <input type="number" id="revTarget" value="5" step="0.5" min="-10" max="25" class="rev-input" />
                        <span class="text-slate-400 font-medium">%</span>
                    </div>
                </div>
                <div>
                    <label class="block text-xs font-bold uppercase tracking-wide text-slate-500 mb-2">Mindestwahrscheinlichkeit</label>
                    <div class="flex items-center gap-2">
                        <input type="number" id="revProb" value="90" step="5" min="50" max="100" class="rev-input" />
                        <span class="text-slate-400 font-medium">%</span>
                    </div>
                </div>
            </div>

            <div class="bg-white border border-slate-200 rounded-xl p-6 min-h-[100px] flex items-center" id="revResult">
                <div class="text-slate-400 text-sm">← Werte eingeben und Enter drücken</div>
            </div>
        </div>

        <div class="text-center text-xs text-slate-400 pb-8 leading-relaxed max-w-2xl mx-auto">
            Datenbasis: MSCI World Renditedreieck · 1925–2025 · 5.050 Start/End-Kombinationen<br>
            Historische Werte sind kein verlässlicher Indikator für zukünftige Ergebnisse. Keine Anlageberatung.
        </div>

    </div>

    <script>{script_code}</script>
</body>
</html>
"""

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Rewrite complete")
