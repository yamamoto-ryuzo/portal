> **注意**  
> このREADMEはAIによって自動生成されたものであり、内容の正確性や最新性について保証されていません。ご利用の際は公式ドキュメント等で必ずご確認ください。

# JavaScriptのマップライブラリ

JavaScriptで利用できる主な地図ライブラリについてまとめています。

## 2D地図ライブラリ

- [Leaflet](https://leafletjs.com/)
  - 軽量・シンプルなオープンソース地図ライブラリ。  
    モバイル端末にも最適化されており、基本的な地図表示やマーカー・ポリゴン・ポリラインの描画が簡単。  
    豊富なプラグインで機能拡張が可能。
  - **主な対応データ形式:** GeoJSON, KML, GPX, CSV, ラスタタイル, ベクトルタイル（プラグイン）
  - 参考: [公式サイト](https://leafletjs.com/) / [埼玉大学谷健二研究室：Leaflet学習](https://ktgis.net/service/leafletlearn/index.html) / [サンプル（地理院タイル・マーカー・ポリゴン）](https://ktgis.net/service/leafletlearn/sample.html)

- [OpenLayers](https://openlayers.org/)
  - 高機能な地図描画・操作ライブラリ。  
    OSMやGeoJSON、KML、WMS、WMTSなど多様な地理空間データ形式に対応。  
    投影変換や編集機能、インタラクションも充実しており、業務用途にも適する。
    ※ 標準では2D地図のみ対応。3D地図表示はサポートしていませんが、[ol-cesium](https://github.com/openlayers/ol-cesium)などの拡張を利用することでCesiumJSと連携した3D表示も可能です。
    - **ol-cesium**はOpenLayersの2D地図とCesiumJSの3D地球表示を同じ地図上で同期・切り替えできるOSSライブラリです。  
      これにより、OpenLayersで作成した地図やレイヤーをそのまま3D地球上に表示したり、2D/3Dをシームレスに切り替えることができます。  
      例: [ol-cesium公式デモ](https://openlayers.org/ol-cesium/examples/synchronization.html)
  - **主な対応データ形式:** GeoJSON, KML, GML, WMS, WMTS, XYZタイル, TopoJSON, GPX, MVT（ベクトルタイル）, ラスタ画像
  - 参考: [公式サイト](https://openlayers.org/) / [OpenLayers入門](https://developer-note.com/ol_entry/) / [サンプル（基本地図・GeoJSON・スタイル変更）](https://yamamoto-ryuzo.github.io/openlayers-map/)

- [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript)
  - Googleが提供する公式地図API。  
    詳細な地図データ、ストリートビュー、ルート検索、ジオコーディングなど多彩なサービスと連携可能。  
    商用利用にはAPIキーと利用料金が必要。
  - **主な対応データ形式:** GeoJSON, KML, Fusion Tables, Google独自の地図・航空写真・地形タイル
  - 参考: [公式サイト](https://developers.google.com/maps/documentation/javascript)

- [Turf.js](https://turfjs.org/)
  - ジオメトリ演算や空間解析用のJavaScriptライブラリ。  
    距離計算、バッファ、クリッピング、集約などGIS的な処理をクライアントサイドで実現。
  - **主な対応データ形式:** GeoJSON（入力・出力ともGeoJSONが基本）
  - 参考: [公式サイト](https://turfjs.org/) / [Qiita解説](https://qiita.com/dayjournal/items/b89a8c650237738c975f)

## 2D/3D対応・3D表示に強いライブラリ

- [MapLibre GL JS](https://maplibre.org/projects/maplibre-gl-js/)
  - Mapbox GL JSのOSSフォーク。  
    ベクトルタイルやラスタタイルの高速描画、地図の3D表示、スタイルの柔軟なカスタマイズが可能。  
    Mapbox Style Specに準拠し、商用・非商用問わず無料で利用できる。
  - **主な対応データ形式:** MVT（Mapbox Vector Tile）, ラスタタイル, GeoJSON, ラスタ画像, Mapbox Style JSON
  - 参考: [公式サイト](https://maplibre.org/maplibre-gl-js/docs/) / [Zenn（あさひなさん記事）](https://zenn.dev/asahina820/books/c29592e397a35b) / [サンプル（ベクトルタイル・スタイル切替）](https://maplibre.org/maplibre-gl-js-docs/example/)

- [Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js/)
  - ベクトルタイルベースの高機能地図ライブラリ。  
    地図のスタイルを自由にカスタマイズでき、3D地図やアニメーションもサポート。  
    商用利用は有償。
  - **主な対応データ形式:** MVT, GeoJSON, ラスタタイル, Mapbox Style JSON, 3D地形（DEM）, 画像オーバーレイ
  - 参考: [公式サイト](https://docs.mapbox.com/mapbox-gl-js/) / [サンプル集](https://docs.mapbox.com/mapbox-gl-js/example/)

- [CesiumJS](https://cesium.com/platform/cesiumjs/)
  - 3D地球・地図可視化ライブラリ。  
    地形や建物の3D表示、時系列アニメーション、各種地理空間データの統合表示が可能。  
    PLATEAUなどの3D都市モデルとも連携。
  - **主な対応データ形式:** 3D Tiles, glTF, CZML, KML, GeoJSON, 点群（LAS/LAZ→3D Tiles変換）, 画像タイル, 地形データ（DEM）
  - 参考: [公式サイト](https://cesium.com/platform/cesiumjs/) / [PLATEAUトピック](https://www.mlit.go.jp/plateau/learning/tpc06-1/) / [サンプル集（3D地球・都市モデル）](https://sandcastle.cesium.com/)

- [deck.gl](https://deck.gl/)
  - WebGLベースの大規模データ可視化フレームワーク。  
    地図上に大量のポイント・ライン・ポリゴン・ヒートマップなどを高パフォーマンスで描画できる。  
    MapLibreやMapbox、Google Maps等と組み合わせて利用可能。  
    3Dレイヤーやアニメーション表現も得意。
  - **主な対応データ形式:** GeoJSON, CSV, 3D Tiles, 点群（LAS/LAZ）, MVT, ラスタ画像, ビッグデータ（Arrow, Parquet等）
  - 参考: [公式サイト](https://deck.gl/) / [Qiita解説](https://qiita.com/keijipoon/items/92d9551930fe52d6c90a) / [サンプル集（大規模データ可視化）](https://deck.gl/examples/)

- [three.js](https://threejs.org/)
  - WebGLを簡単に扱えるJavaScript 3Dグラフィックスライブラリ。  
    地形や建物などの3Dオブジェクトをブラウザ上で自由に表現でき、QGIS2threejsなどのツールでも利用されている。  
    地図専用ではないが、3D地図や都市モデルの可視化にも活用される。
  - **主な対応データ形式:** glTF, OBJ, FBX, STL, Collada, PLY, 画像テクスチャ, 点群（PLY, LAS/LAZ等は変換要）
  - 参考: [公式サイト](https://threejs.org/) / [サンプル集（3D表現全般）](https://threejs.org/examples/)

- [Potree](https://potree.org/)
  - WebGLベースのオープンソース点群データ可視化ライブラリ。  
    大規模なLAS/LAZ形式などの点群データをWebブラウザ上で高速かつインタラクティブに表示できる。  
    地形や建物の3Dスキャンデータ、測量データの可視化に最適で、属性情報の表示や断面計測などの機能も豊富。
  - **主な対応データ形式:** LAS, LAZ, PotreeConverterで変換したBIN, PLY, XYZ, PTX, CSV（点群）
  - 参考: [公式サイト](https://potree.org/) / [サンプル集](https://potree.org/demo.html)

## 主なデータ形式と対応ライブラリ

### 2Dデータ形式

| データ形式         | 概要・用途                                   | 主な対応ライブラリ                       | 備考・変換例                       |
|--------------------|----------------------------------------------|------------------------------------------|------------------------------------|
| GeoJSON            | 2D/3D地理空間データ（属性付）                | Leaflet, OpenLayers, MapLibre GL JS, Mapbox GL JS, CesiumJS, deck.gl, Turf.js | 多くのWeb地図で標準対応            |
| KML                | Google系やGISで使われるXML地理データ          | Leaflet, OpenLayers, Google Maps, CesiumJS |                                    |
| GPX                | GPSトラックデータ                            | Leaflet, OpenLayers                      |                                    |
| CSV                | 座標付きテーブルデータ                       | Leaflet, OpenLayers, deck.gl             |                                    |
| TopoJSON           | GeoJSONの拡張（トポロジー情報）               | OpenLayers, deck.gl                      |                                    |
| GML                | OGC標準のXML地理データ                       | OpenLayers                               |                                    |
| MVT（ベクトルタイル）| 高速な地図描画用ベクトルタイル               | MapLibre GL JS, Mapbox GL JS, OpenLayers, deck.gl |                                  |
| ラスタタイル       | 地図画像タイル（XYZ, WMTS, WMS等）           | Leaflet, OpenLayers, MapLibre GL JS, Mapbox GL JS |                              |
| 画像オーバーレイ   | 任意画像の地図重ね合わせ                     | Leaflet, OpenLayers, Mapbox GL JS        |                                    |
| Mapbox Style JSON  | 地図スタイル定義                             | MapLibre GL JS, Mapbox GL JS             |                                    |

### 3Dデータ形式

| データ形式         | 概要・用途                                   | 主な対応ライブラリ                       | 備考・変換例                       |
|--------------------|----------------------------------------------|------------------------------------------|------------------------------------|
| 3D Tiles           | 大規模3D地理空間データ配信                   | CesiumJS, deck.gl                        | CityGML/IFC/点群→3D Tiles変換可    |
| glTF               | 軽量3Dモデル                                 | CesiumJS, three.js                       | IFC/OBJ/FBX→glTF変換可             |
| OBJ/FBX/STL/PLY    | 汎用3Dモデル                                 | three.js                                 | glTF変換推奨                       |
| LAS/LAZ            | 点群データ                                   | deck.gl, Potree, CesiumJS（3D Tiles変換）| PotreeConverter等で変換可           |
| CityGML            | 都市モデルXML                                | CesiumJS（3D Tiles変換）, FME            | PLATEAU等                          |
| CZML               | 時系列3D地理データ                           | CesiumJS                                 |                                    |
| DEM                | 標高・地形ラスタデータ                       | CesiumJS, Mapbox GL JS                   |                                    |

- ※各ライブラリの詳細やサンプルは上記のライブラリ紹介欄を参照してください。
- データ形式によっては、事前に変換（例：IFC→glTF/3D Tiles、CityGML→3D Tiles、LAS→Potree形式など）が必要な場合があります。

## QGISとの連携

- QGISで作成したGeoJSONやシェープファイルをエクスポートし、LeafletやOpenLayers、MapLibre GL JSなどのJavaScriptライブラリでWeb地図として表示できます。
- [QGIS2Web](https://github.com/tomchadwin/qgis2web)プラグインを使うと、QGISのプロジェクトをそのままLeafletやOpenLayers用のHTMLにエクスポート可能です。
- PLATEAUや3D都市モデルのデータをQGISで加工し、CesiumJSやdeck.glでWeb可視化する事例も増えています。
- QGISでスタイリングしたベクトルタイル（MVT）をMapLibre GL JSやMapbox GL JSで利用することも可能です。
- **QGIS2threejs**プラグインを使うと、QGISの3D地形や建物データをWebGLベースの3D地図（three.js利用）としてエクスポートできます。  
  [QGIS2threejs公式ページ](https://qgis2threejs.readthedocs.io/ja/latest/) / [サンプル（QGISから3D出力）](https://qgis2threejs.readthedocs.io/ja/latest/sample.html)
  - ※ QGIS2threejsは[three.js](https://threejs.org/)というJavaScript 3Dグラフィックスライブラリを利用しています。

## BIM/CIMとの連携

- BIM（Building Information Modeling）やCIM（Construction Information Modeling）で作成された3Dモデルや属性情報は、Web地図・3D地図ライブラリと連携して可視化・共有が可能です。
- 主なデータ形式例：
    - **IFC（Industry Foundation Classes）**: 建築・土木分野で標準的なBIMデータ交換フォーマット。直接Web地図で表示するには変換が必要（例：glTFや3D Tilesへ）。
    - **glTF（GL Transmission Format）**: 軽量な3Dモデルフォーマット。three.jsやCesiumJSで直接読み込み・表示が可能。
    - **3D Tiles**: CesiumJSが提唱する大規模3D地理空間データ配信フォーマット。BIM/CIMや点群データ、都市モデル（PLATEAU等）で利用。
    - **CityGML**: 都市モデルのXMLベース標準。FMEやPLATEAUツール等で3D TilesやglTFに変換してWeb可視化。
    - **OBJ/FBX**: 3D CADやBIMソフトでよく使われる汎用3Dモデルフォーマット。three.js等で利用可能（glTF変換推奨）。
    - **LAS/LAZ**: 点群データフォーマット。deck.glやPotree等で可視化可能。
    - **GeoJSON/TopoJSON**: 属性付き2D/3D地理空間データ。地図ライブラリで広く利用。

- [CesiumJS](https://cesium.com/platform/cesiumjs/)はglTFや3D Tiles形式に対応しており、BIM/CIMデータを大規模かつ高精度にWebブラウザ上で表示できます。
- [three.js](https://threejs.org/)もglTFやOBJ等の3Dモデルを読み込んで表示でき、BIM/CIMデータのカスタム可視化やインタラクションも実現可能です。
- [deck.gl](https://deck.gl/)は3D Tilesや点群データ（LAS/LAZ）の可視化にも対応しています。
- QGISやFME等のGISツールを使ってBIM/CIMデータをGeoJSON、3D Tiles、glTF等に変換し、Web地図ライブラリで利用する事例も増えています。
- PLATEAUプロジェクトのような都市モデル（CityGML/3D Tiles）もCesiumJSやdeck.glで活用されています。

## データ形式とライブラリの関係

- Web地図・3D地図ライブラリは、それぞれ対応するデータ形式が異なります。  
  例えば、**Leaflet**や**OpenLayers**はGeoJSONやKMLなどの2D地理空間データに強く、**MapLibre GL JS**や**Mapbox GL JS**はベクトルタイル（MVT）やラスタタイルの高速描画に特化しています。
- 3Dモデルや都市モデル、点群データをWebで可視化したい場合は、**CesiumJS**（3D Tiles, glTF, CityGML変換）、**three.js**（glTF, OBJ, FBX等）、**deck.gl**（3D Tiles, LAS/LAZ等）、**Potree**（LAS/LAZ, PLY等点群）など、用途に応じて適切なライブラリとデータ形式を選択する必要があります。
- データ形式によっては、事前に変換（例：IFC→glTF/3D Tiles、CityGML→3D Tiles、LAS→Potree形式など）が必要な場合があります。
- 目的の可視化やインタラクション、データ容量、パフォーマンス要件に応じて、ライブラリとデータ形式の組み合わせを検討してください。

## その他参考リンク

- [GIS実習オープン教材](https://gis-oer.github.io/gitbook/book/materials/web_gis/)
- [地理院タイルを用いたサイト構築サンプル集](https://maps.gsi.go.jp/development/sample.html)
- [電子版書籍：「JavaScriptではじめるWebマップアプリケーション」](https://techbookfest.org/product/5707841755152384?productVariantID=5181910525411328)