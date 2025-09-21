// app/routes/_index.tsx
import { redirect, type LoaderFunctionArgs } from "@remix-run/node";

export async function loader({ request }: LoaderFunctionArgs) {
  const url = new URL(request.url);
  const shop = url.searchParams.get("shop");

  if (shop) {
    // Din app-slug/handle i Admin (sätt APP_HANDLE som env i Vercel)
    const handle = process.env.APP_HANDLE ?? "prisjakt-produktfeed";
    const adminUrl = `https://admin.shopify.com/store/${shop}/apps/${encodeURIComponent(handle)}`;
    return redirect(adminUrl);
  }

  // Enkel landningssida om man går till / utan ?shop=
  return new Response(
    `<!doctype html>
     <html>
       <head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
       <body style="font-family:system-ui;padding:24px;max-width:640px">
         <h1>Prisjakt Produktfeed</h1>
         <p>Skriv din butiksadress (ex: <code>nordic-aim-sandbox.myshopify.com</code>)</p>
         <form onsubmit="event.preventDefault();
                         var s=document.getElementById('shop').value.trim();
                         if(!s) return;
                         var h=${JSON.stringify(process.env.APP_HANDLE ?? "prisjakt-produktfeed")};
                         var u='https://admin.shopify.com/store/'+s+'/apps/'+encodeURIComponent(h);
                         window.location.href=u;">
           <input id="shop" placeholder="din-butik.myshopify.com" style="width:100%;padding:8px"/>
           <div style="margin-top:8px"><button type="submit" style="padding:8px 12px">Öppna appen</button></div>
         </form>
       </body>
     </html>`,
    { headers: { "Content-Type": "text/html; charset=utf-8" } }
  );
}

export default function Index() {
  return null;
}
