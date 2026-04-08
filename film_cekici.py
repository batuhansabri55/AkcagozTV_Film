export default {
  // --- 1. OTOMATİK KONTROL (CRON) ---
  async scheduled(event, env, ctx) {
    ctx.waitUntil(this.handleHealthCheck(env));
  },

  // --- 2. ANA FETCH MANTIĞI ---
  async fetch(request, env) {
    const dbUrl = "https://batuhansabri-batuhansabri.aws-eu-west-1.turso.io/v2/pipeline";
    const dbToken = env.DB_TOKEN || "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3NzQ4ODgxNTQsImlkIjoiMDE5ZDNmMTctM2EwMS03ZDcyLWFkZWEtNGJhYjM2ZWU4NzkwIiwicmlkIjoiOGE2MjQ5ZDctNTY5MS00MzUwLTkxZjYtNTM4MDFjMjQzOGRmIn0.PbPxOVppUF363-GvC_wsFDPEuMPS1fepM_PUrQjJeDm1Hn5fnPGWL5mhPJhWCCuOKt8ws0BIXfzY1AP47bHcAQ";
    const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36";

    async function queryTurso(requests) {
      try {
        const res = await fetch(dbUrl, {
          method: "POST",
          headers: { "Authorization": `Bearer ${dbToken}`, "Content-Type": "application/json" },
          body: JSON.stringify({ requests })
        });
        const json = await res.json();
        return json.results || [];
      } catch (e) { return []; }
    }

    const url = new URL(request.url);
    const origin = url.origin;

    // --- [YENİ] VİDEO PARSER (FİLM/DİZİ ÇÖZÜCÜ) ---
    if (url.pathname === "/parse") {
      const target = url.searchParams.get("url");
      if (!target) return new Response("URL Eksik", { status: 400 });

      try {
        const response = await fetch(target, { headers: { "User-Agent": UA } });
        const html = await response.text();
        let finalLink = "";

        // Film Makinesi & DiziBOX & Dizipub Mantığı (Regex ile Kaynaktan Ayıklama)
        if (target.includes("filmmakinesi")) {
          finalLink = html.match(/file:"(.*?)"/)?.[1] || html.match(/source src="(.*?)"/)?.[1];
        } else if (target.includes("dizilla") || target.includes("dizipub")) {
          finalLink = html.match(/source: "(.*?)"/)?.[1] || html.match(/file: '(.*?)'/)?.[1];
        } else if (target.includes("filmmodu")) {
          finalLink = html.match(/src='(.*?)'/)?.[1];
        }

        // Eğer link bir iframe ise, içindeki gerçek videoyu bir tur daha çözmeye çalışır
        if (finalLink && finalLink.includes("iframe")) {
           const frameRes = await fetch(finalLink, { headers: { "Referer": target } });
           const frameHtml = await frameRes.text();
           finalLink = frameHtml.match(/file:"(.*?)"/)?.[1] || finalLink;
        }

        return Response.redirect(finalLink || target, 302);
      } catch (e) {
        return Response.redirect(target, 302);
      }
    }

    // --- KANAL LİSTESİ (M3U) ---
    if (url.pathname === "/list") {
      const isTest = url.searchParams.get("test");
      if (isTest !== "1") {
        const cachedList = await env.MY_KV.get("HIZLI_LISTE");
        if (cachedList && cachedList.length > 500) {
          return new Response(cachedList, { headers: { "Content-Type": "text/plain; charset=UTF-8" } });
        }
      }
    }

    // --- KRİTİK OYNATICI VE AGRESİF TEST (600ms) ---
    if (url.pathname === "/play") {
      const name = url.searchParams.get("name");
      const res = await queryTurso([
        { type: "execute", stmt: { sql: "SELECT url FROM channels WHERE name=?", args: [{type:"text", value:name}] } },
        { type: "execute", stmt: { sql: "SELECT backup_url FROM channel_backups WHERE channel_name=? AND status=1 ORDER BY backup_order ASC", args: [{type:"text", value:name}] } }
      ]);
      const mR = res[0]?.response?.result?.rows[0]?.[0]?.value || "";
      const bL = (res[1]?.response?.result?.rows || []).map(r => r[0].value);
      const skip = ["0", "SKIP", "PASS", "OFFLINE", "NULL", ""];
      let isBroken = skip.includes(mR.trim().toUpperCase()) || !mR.startsWith("http");
      let links = isBroken ? bL.filter(u => u?.startsWith("http")) : [mR, ...bL].filter(u => u?.startsWith("http"));
      
      for (let link of links) {
        try {
          const controller = new AbortController();
          const timeoutId = setTimeout(() => controller.abort(), 600);
          const c = await fetch(link, { 
            method: "GET", 
            headers: { "User-Agent": UA, "Range": "bytes=0-1" },
            signal: controller.signal,
            cf: { timeout: 600 } 
          });
          clearTimeout(timeoutId);
          if (c.ok || c.status === 206) {
            if (isBroken || link !== mR) {
              await queryTurso([{ type: "execute", stmt: { sql: "UPDATE channels SET url = ? WHERE name = ?", args: [{type:"text", value:link}, {type:"text", value:name}] } }]);
            }
            await queryTurso([{ type: "execute", stmt: { sql: "INSERT OR REPLACE INTO settings (key, value) VALUES ('active_stream', ?)", args: [{type:"text", value: "🎬 " + name + " | 🔗 " + link}] } }]);
            return Response.redirect(link, 302);
          }
        } catch (e) { continue; }
      }
      return Response.redirect(links[0] || "about:blank", 302);
    }

    // --- MODERN PANEL VE DASHBOARD ---
    const all = await queryTurso([
      { type: "execute", stmt: { sql: "SELECT * FROM channels ORDER BY name ASC" } },
      { type: "execute", stmt: { sql: "SELECT * FROM channel_backups" } },
      { type: "execute", stmt: { sql: "SELECT value FROM settings WHERE key='active_stream'" } }
    ]);

    const chs = all[0]?.response?.result || { rows: [], cols: [] };
    const bd = all[1]?.response?.result || { rows: [], cols: [] };
    const live = all[2]?.response?.result?.rows[0]?.[0]?.value || "Sinyal Bekleniyor...";
    
    // UI Kodları Buraya Gelecek (Dün verdiğim o modern Dashboard HTML'i)
    return new Response(`...HTML KODLARI...`, { headers: { "Content-Type": "text/html; charset=UTF-8" } });
  },

  async handleHealthCheck(env) {
    // Arka plan kontrol kodları
  }
};
