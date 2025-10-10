// app/routes/_index.tsx
import { redirect, type LoaderFunctionArgs } from "@remix-run/node";

function toStoreSlug(input: string) {
  const s = input.trim().toLowerCase();
  return s.replace(/\.myshopify\.com$/, "");
}

export async function loader({ request }: LoaderFunctionArgs) {
  const url = new URL(request.url);
  const shopParam = url.searchParams.get("shop");

  if (shopParam) {
    const slug = toStoreSlug(shopParam);
    const handle = process.env.APP_HANDLE ?? "prisjakt-produktfeed";
    const adminUrl = `https://admin.shopify.com/store/${encodeURIComponent(
      slug
    )}/apps/${encodeURIComponent(handle)}/app`;
    return redirect(adminUrl);
  }

  return new Response(
    `<!doctype html>
     <html>
       <head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
       <body style="font-family:system-ui;padding:24px;max-width:640px">
         <h1>Prisjakt Produktfeed</h1>
         <p>Skriv din butiksadress (t.ex. <code>nordic-aim-sandbox.myshopify.com</code>)</p>
         <form onsubmit="event.preventDefault();
                         var v=document.getElementById('shop').value.trim();
                         if(!v) return;
                         var slug=v.toLowerCase().replace(/\\.myshopify\\.com$/, '');
                         var h=${JSON.stringify(process.env.APP_HANDLE ?? "prisjakt-produktfeed")};
                         var u='https://admin.shopify.com/store/'+encodeURIComponent(slug)+'/apps/'+encodeURIComponent(h)+'/app';
                         window.location.href=u;">
           <input id="shop" placeholder="din-butik.myshopify.com" style="width:100%;padding:8px"/>
           <div style="margin-top:8px"><button type="submit" style="padding:8px 12px">Öppna appen</button></div>
         </form>
       </body>
     </html>`,
    { headers: { "Content-Type": "text/html; charset=utf-8" } }
  );
}

export default function Index() { return null; }
