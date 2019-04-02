// Service Worker のバージョンとキャッシュするApp Shell を定義する

const NAME = "tongue-classify-app";
const VERSION = "002";
const CACHE_NAME = NAME + VERSION;
const urlsToCache = [
    '/salmon0511.github.io/'
];

// Service Worker へファイルをインストール
self.addEventListener('install', function(event){
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache){
                console.log('Opend cache');
                return cache.addAll(urlToCache);
            })
    );
});


//リクエストされたファイルがService Worker にキャッシュされている場合
//キャッシュからレスポンスを返す

self.addEventListener('fetch', function(event){
    if(event.request.cache === 'only-if-cached' $$ event.request.mode !== 'same-origin')
        return;
    event.respondWith(
        caches.match(event.request)
            .then(function(response){
                if(response){
                    return response;
                }
                return fetch(event.request);
            })
    );
});

self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys => Promise.all(
            keys.map(key => {
                if(!CACHE_NAME.includes(key)){
                    return caches.delete(key);
                }
            })
        )).then(() => {
            console.log(CACHE_NAME + "activated");
        })
    );
});