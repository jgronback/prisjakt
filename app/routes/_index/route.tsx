// app/routes/_index/route.tsx
import type { LoaderFunctionArgs } from "@remix-run/node";

export async function loader({ request }: LoaderFunctionArgs) {
  const url = new URL(request.url);
  const shop = url.searchParams.get("shop");
  if (shop) {
    const handle = process.env.APP_HANDLE || "prisjakt-produktfeed";
    const adminUrl = `https://admin.shopify.com/store/${shop}/apps/${encodeURIComponent(handle)}`;
    return new Response(
      `<!doctype html><html><body><script>
         if (window.top) window.top.location.href=${JSON.stringify(adminUrl)};
         else window.location.href=${JSON.stringify(adminUrl)};
       </script></body></html>`,
      { headers: { "Content-Type": "text/html" } }
    );
  }

  // Fallback: enkel landningssida där man kan skriva in shop manuellt
  return new Response(
    `<!doctype html>
     <html><body style="font-family:system-ui; padding:24px; max-width:640px">
       <h1>Prisjakt Produktfeed</h1>
       <p>Skriv din butiksadress (ex: <code>nordic-aim-sandbox.myshopify.com</code>)</p>
       <form onsubmit="event.preventDefault(); var s=document.getElementById('shop').value.trim(); if(!s) return; var h=${JSON.stringify(process.env.APP_HANDLE || "prisjakt-produktfeed")};
         var u='https://admin.shopify.com/store/'+s+'/apps/'+encodeURIComponent(h);
         if (window.top) window.top.location.href=u; else window.location.href=u;">
         <input id="shop" placeholder="din-butik.myshopify.com" style="width:100%;padding:8px"/>
         <div style="margin-top:8px"><button type="submit" style="padding:8px 12px">Öppna appen</button></div>
       </form>
     </body></html>`,
    { headers: { "Content-Type": "text/html" } }
  );
}

export default function Index() {
  return null;
}
