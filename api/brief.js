// The earlier unrelated news feed has been retired. Existing API clients get an explicit migration response.
export default function handler(req,res){res.setHeader('Cache-Control','no-store');return res.status(410).json({error:'Rivet now plans public comments; the news API is retired.',replacement:'/api/opportunities',schema:'rivet-opportunities/2'});}
