> **注意**  
> このREADMEはAIによって自動生成されたものであり、内容の正確性や最新性について保証されていません。ご利用の際は公式ドキュメント等で必ずご確認ください。

# JavaScriptのマップライブラリ

JavaScriptで利用できる主な地図ライブラリについてまとめています。

## 2D地図ライブラリ

- [Leaflet](https://leafletjs.com/)
  - 軽量・シンプルなオープンソース地図ライブラリ。  
    モバイル端末にも最適化されており、基本的な地図表示やマーカー・ポリゴン・ポリラインの描画が簡単。  
    豊富なプラグインで機能拡張が可能。
  - 参考: [公式サイト](https://leafletjs.com/) / [埼玉大学谷健二研究室：Leaflet学習](https://ktgis.net/service/leafletlearn/index.html) / [サンプル（地理院タイル・マーカー・ポリゴン）](https://ktgis.net/service/leafletlearn/sample.html)

- [OpenLayers](https://openlayers.org/)
  - 高機能な地図描画・操作ライブラリ。  
    OSMやGeoJSON、KML、WMS、WMTSなど多様な地理空間データ形式に対応。  
    投影変換や編集機能、インタラクションも充実しており、業務用途にも適する。
    ※ 標準では2D地図のみ対応。3D地図表示はサポートしていませんが、[ol-cesium](https://github.com/openlayers/ol-cesium)などの拡張を利用することでCesiumJSと連携した3D表示も可能です。
    - **ol-cesium**はOpenLayersの2D地図とCesiumJSの3D地球表示を同じ地図上で同期・切り替えできるOSSライブラリです。  
      これにより、OpenLayersで作成した地図やレイヤーをそのまま3D地球上に表示したり、2D/3Dをシームレスに切り替えることができます。  
      例: [ol-cesium公式デモ](https://openlayers.org/ol-cesium/examples/synchronization.html)
  - 参考: [公式サイト](https://openlayers.org/) / [OpenLayers入門](https://developer-note.com/ol_entry/) / [サンプル（基本地図・GeoJSON・スタイル変更）](https://yamamoto-ryuzo.github.io/openlayers-map/)

- [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript)
  - Googleが提供する公式地図API。  
    詳細な地図データ、ストリートビュー、ルート検索、ジオコーディングなど多彩なサービスと連携可能。  
    商用利用にはAPIキーと利用料金が必要。
  - 参考: [公式サイト](https://developers.google.com/maps/documentation/javascript)

- [Turf.js](https://turfjs.org/)
  - ジオメトリ演算や空間解析用のJavaScriptライブラリ。  
    距離計算、バッファ、クリッピング、集約などGIS的な処理をクライアントサイドで実現。
  - 参考: [公式サイト](https://turfjs.org/) / [Qiita解説](https://qiita.com/dayjournal/items/b89a8c650237738c975f)

## 2D/3D対応・3D表示に強いライブラリ

- [MapLibre GL JS](https://maplibre.org/projects/maplibre-gl-js/)
  - Mapbox GL JSのOSSフォーク。  
    ベクトルタイルやラスタタイルの高速描画、地図の3D表示、スタイルの柔軟なカスタマイズが可能。  
    Mapbox Style Specに準拠し、商用・非商用問わず無料で利用できる。
  - 参考: [公式サイト](https://maplibre.org/maplibre-gl-js/docs/) / [Zenn（あさひなさん記事）](https://zenn.dev/asahina820/books/c29592e397a35b) / [サンプル（ベクトルタイル・スタイル切替）](https://maplibre.org/maplibre-gl-js-docs/example/)

- [Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js/)
  - ベクトルタイルベースの高機能地図ライブラリ。  
    地図のスタイルを自由にカスタマイズでき、3D地図やアニメーションもサポート。  
    商用利用は有償。
  - 参考: [公式サイト](https://docs.mapbox.com/mapbox-gl-js/) / [サンプル集](https://docs.mapbox.com/mapbox-gl-js/example/)

- [CesiumJS](https://cesium.com/platform/cesiumjs/)
  - 3D地球・地図可視化ライブラリ。  
    地形や建物の3D表示、時系列アニメーション、各種地理空間データの統合表示が可能。  
    PLATEAUなどの3D都市モデルとも連携。
  - 参考: [公式サイト](https://cesium.com/platform/cesiumjs/) / [PLATEAUトピック](https://www.mlit.go.jp/plateau/learning/tpc06-1/) / [サンプル集（3D地球・都市モデル）](https://sandcastle.cesium.com/)

- [deck.gl](https://deck.gl/)
  - WebGLベースの大規模データ可視化フレームワーク。  
    地図上に大量のポイント・ライン・ポリゴン・ヒートマップなどを高パフォーマンスで描画できる。  
    MapLibreやMapbox、Google Maps等と組み合わせて利用可能。  
    3Dレイヤーやアニメーション表現も得意。
  - 参考: [公式サイト](https://deck.gl/) / [Qiita解説](https://qiita.com/keijipoon/items/92d9551930fe52d6c90a) / [サンプル集（大規模データ可視化）](https://deck.gl/examples/)

- [three.js](https://threejs.org/)
  - WebGLを簡単に扱えるJavaScript 3Dグラフィックスライブラリ。  
    地形や建物などの3Dオブジェクトをブラウザ上で自由に表現でき、QGIS2threejsなどのツールでも利用されている。  
    地図専用ではないが、3D地図や都市モデルの可視化にも活用される。
  - 参考: [公式サイト](https://threejs.org/) / [サンプル集（3D表現全般）](https://threejs.org/examples/)

## QGISとの連携

- QGISで作成したGeoJSONやシェープファイルをエクスポートし、LeafletやOpenLayers、MapLibre GL JSなどのJavaScriptライブラリでWeb地図として表示できます。
- [QGIS2Web](https://github.com/tomchadwin/qgis2web)プラグインを使うと、QGISのプロジェクトをそのままLeafletやOpenLayers用のHTMLにエクスポート可能です。
- PLATEAUや3D都市モデルのデータをQGISで加工し、CesiumJSやdeck.glでWeb可視化する事例も増えています。
- QGISでスタイリングしたベクトルタイル（MVT）をMapLibre GL JSやMapbox GL JSで利用することも可能です。
- **QGIS2threejs**プラグインを使うと、QGISの3D地形や建物データをWebGLベースの3D地図（three.js利用）としてエクスポートできます。  
  [QGIS2threejs公式ページ](https://qgis2threejs.readthedocs.io/ja/latest/) / [サンプル（QGISから3D出力）](https://qgis2threejs.readthedocs.io/ja/latest/sample.html)
  - ※ QGIS2threejsは[three.js](https://threejs.org/)というJavaScript 3Dグラフィックスライブラリを利用しています。

## その他参考リンク

- [GIS実習オープン教材](https://gis-oer.github.io/gitbook/book/materials/web_gis/)
- [地理院タイルを用いたサイト構築サンプル集](https://maps.gsi.go.jp/development/sample.html)
- [電子版書籍：「JavaScriptではじめるWebマップアプリケーション」](https://techbookfest.org/product/5707841755152384?productVariantID=5181910525411328)

## その他参考リンク

- [GIS実習オープン教材](https://gis-oer.github.io/gitbook/book/materials/web_gis/)
- [地理院タイルを用いたサイト構築サンプル集](https://maps.gsi.go.jp/development/sample.html)
- [電子版書籍：「JavaScriptではじめるWebマップアプリケーション」](https://techbookfest.org/product/5707841755152384?productVariantID=5181910525411328)
