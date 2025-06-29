> **注意**  
> このREADMEはAIによって自動生成されたものであり、内容の正確性や最新性について保証されていません。ご利用の際は公式ドキュメント等で必ずご確認ください。

# JavaScriptのマップライブラリ

## 目次

- [はじめに](#はじめに)
- [WebGLとは](#webglとは)
- [2D地図ライブラリ](#2d地図ライブラリ)
- [2D/3D対応・3D表示に強いライブラリ](#2d3d対応3d表示に強いライブラリ)
- [主なデータ形式と対応ライブラリ](#主なデータ形式と対応ライブラリ)
  - [2Dデータ形式](#2dデータ形式)
  - [3Dデータ形式](#3dデータ形式)
  - [データ形式変換・生成に役立つ主なツール・ライブラリ](#データ形式変換生成に役立つ主なツールライブラリ)
- [QGIS・AutoCAD・ArcGIS・BIM/CIMとの連携](#qgisautocadarcgisbimcimとの連携)
- [3D・VR・AR・MRとの関係](#3dvrarmrとの関係)
- [代表的なサービス・アプリと3D・VR・AR・MRとの関係](#代表的なサービスアプリと3dvrarmrとの関係)

---

## はじめに

JavaScriptで利用できる主な地図ライブラリについてまとめています。

## WebGLとは

[▲目次へ戻る](#目次)

WebGL（Web Graphics Library）は、Webブラウザ上でハードウェアアクセラレーションを利用した3D/2Dグラフィックスを描画するためのJavaScript APIです。  
WebGLを利用することで、インストール不要で高性能な3D地図や都市モデル、点群データなどの可視化が可能となり、three.js、Babylon.js、CesiumJS、deck.glなど多くのWeb地図・3D可視化ライブラリの基盤技術となっています。

---

### AutoCAD等のネイティブアプリとWebGLベース可視化の違い

| 項目                | AutoCAD等ネイティブアプリ                | WebGLベース（three.js, CesiumJS等）         |
|---------------------|------------------------------------------|--------------------------------------------|
| 表示性能            | 高速・大規模データも快適（GPU/CPU最適化）| ブラウザ依存・大規模データは工夫が必要      |
| 表示精度            | CAD/BIMの設計精度（ミリ単位・属性も厳密） | 軽量化・簡略化前提（glTF/3D Tiles等は簡易化や座標誤差あり）|
| データ互換性        | DWG/DXF等のCAD/BIMネイティブ形式を直接扱える | glTF, 3D Tiles, OBJ等Web向け軽量形式が主流 |
| 機能                | 精密な作図・編集・属性管理・自動化等が豊富 | 主に可視化・簡易編集・インタラクション      |
| 拡張性              | プラグイン・APIで高度なカスタマイズ可能   | JavaScriptで柔軟に拡張・Web連携が容易      |
| コラボレーション    | ファイル共有・クラウド連携（製品依存）    | URL共有・Web公開・多端末対応が容易         |
| 利用環境            | 専用アプリのインストールが必要            | ブラウザのみで動作・クロスプラットフォーム |
| VR/AR/MR対応        | 一部製品で対応（例：Autodesk VRED等）     | WebXR等で容易に対応・実装事例が多い        |
| コスト              | 商用ライセンスが必要な場合が多い          | OSS/無料ライブラリが多い                   |

- **表示性能・精度について**  
  ネイティブアプリ（AutoCAD等）はGPU/CPU最適化により数百万要素の大規模データも高精度・高速に表示可能で、設計精度（ミリ単位や属性の厳密性）も維持されます。  
  一方、WebGLベースの可視化はブラウザの制約やネットワーク転送の都合上、データ軽量化（LOD・簡略化・座標丸め等）が前提となるため、超高精度な設計用途や厳密な属性管理には向きません。ただし都市モデルや点群の「見せる・共有する」用途では十分な性能・精度を実現できます。  
  表示の滑らかさや応答性は、データ量・端末性能・WebGL実装・最適化手法（タイル分割・LOD・ストリーミング等）に大きく依存します。

---

## 2D地図ライブラリ

[▲目次へ戻る](#目次)

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

[▲目次へ戻る](#目次)

### 2D・3D両対応のライブラリ

- [MapLibre GL JS](https://maplibre.org/projects/maplibre-gl-js/)
  - Mapbox GL JSのOSSフォーク。  
    ベクトルタイルやラスタタイルの高速描画、地図の3D表示（建物の高さ表現や地形起伏）、スタイルの柔軟なカスタマイズが可能。  
    2D/3Dの切り替えや重ね合わせもできる。
  - **主な対応データ形式:** MVT（Mapbox Vector Tile）, ラスタタイル, GeoJSON, ラスタ画像, Mapbox Style JSON
  - 参考: [公式サイト](https://maplibre.org/maplibre-gl-js/docs/) / [Zenn（あさひなさん記事）](https://zenn.dev/asahina820/books/c29592e397a35b) / [サンプル（ベクトルタイル・スタイル切替）](https://maplibre.org/maplibre-gl-js-docs/example/)

- [Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js/)
  - ベクトルタイルベースの高機能地図ライブラリ。  
    2D/3D地図の切り替えや3D地形・建物表現、アニメーションもサポート。  
    商用利用は有償。
  - **主な対応データ形式:** MVT, GeoJSON, ラスタタイル, Mapbox Style JSON, 3D地形（DEM）, 画像オーバーレイ
  - 参考: [公式サイト](https://docs.mapbox.com/mapbox-gl-js/) / [サンプル集](https://docs.mapbox.com/mapbox-gl-js/example/)

- [deck.gl](https://deck.gl/)
  - WebGLベースの大規模データ可視化フレームワーク。  
    2D/3D両方の地図・データ可視化に対応し、MapLibreやMapbox、Google Maps等と組み合わせて利用可能。  
    3Dレイヤーやアニメーション表現も得意。
  - **主な対応データ形式:** GeoJSON, CSV, 3D Tiles, 点群（LAS/LAZ）, MVT, ラスタ画像, ビッグデータ（Arrow, Parquet等）
  - 参考: [公式サイト](https://deck.gl/) / [Qiita解説](https://qiita.com/keijipoon/items/92d9551930fe52d6c90a) / [サンプル集（大規模データ可視化）](https://deck.gl/examples/)

### 3D専用ライブラリ

- [CesiumJS](https://cesium.com/platform/cesiumjs/)
  - 3D地球・地図可視化ライブラリ。  
    地形や建物の3D表示、時系列アニメーション、各種地理空間データの統合表示が可能。  
    PLATEAUなどの3D都市モデルとも連携。
  - **主な対応データ形式:** 3D Tiles, glTF, CZML, KML, GeoJSON, 点群（LAS/LAZ→3D Tiles変換）, 画像タイル, 地形データ（DEM）
  - 参考: [公式サイト](https://cesium.com/platform/cesiumjs/) / [PLATEAUトピック](https://www.mlit.go.jp/plateau/learning/tpc06-1/) / [サンプル集（3D地球・都市モデル）](https://sandcastle.cesium.com/)

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

- [Babylon.js](https://www.babylonjs.com/)
  - 高機能なWebGLベースの3Dエンジン。  
    物理演算やPBRマテリアル、アニメーション、VR/AR（WebXR）などに対応し、都市モデルやBIMデータの可視化・インタラクションも可能。  
    glTFやOBJ、STLなど多様な3Dフォーマットをサポートし、three.jsと並ぶWeb3D開発の代表的ライブラリ。
  - **主な対応データ形式:** glTF, OBJ, STL, Babylon専用形式（.babylon）, 画像テクスチャ
  - 参考: [公式サイト](https://www.babylonjs.com/) / [サンプル集](https://playground.babylonjs.com/)

## 主なデータ形式と対応ライブラリ

### 2Dデータ形式

[▲目次へ戻る](#目次)

| データ形式         | 概要・用途                                   | 主な対応ライブラリ                       | 備考・変換例                       |
|--------------------|----------------------------------------------|------------------------------------------|------------------------------------|
| GeoJSON            | 2D/3D地理空間データ（属性付）                | Leaflet, OpenLayers, MapLibre GL JS, Mapbox GL JS, CesiumJS, deck.gl, Turf.js | 多くのWeb地図で標準対応            |
| KML                | Google系やGISで使われるXML地理データ          | Leaflet, OpenLayers, Google Maps, CesiumJS | ogr2ogr, QGISでGeoJSON等に変換可   |
| GPX                | GPSトラックデータ                            | Leaflet, OpenLayers                      | ogr2ogr, QGISでGeoJSON等に変換可   |
| CSV                | 座標付きテーブルデータ                       | Leaflet, OpenLayers, deck.gl             | QGIS, csv2geojson等でGeoJSON変換可 |
| TopoJSON           | GeoJSONの拡張（トポロジー情報）               | OpenLayers, deck.gl                      | mapshaper等でGeoJSON⇔TopoJSON変換  |
| GML                | OGC標準のXML地理データ                       | OpenLayers                               | ogr2ogr, QGISでGeoJSON等に変換可   |
| MVT（ベクトルタイル）| 高速な地図描画用ベクトルタイル               | MapLibre GL JS, Mapbox GL JS, OpenLayers, deck.gl | tippecanoe, QGIS, ogr2ogrで生成   |
| ラスタタイル       | 地図画像タイル（XYZ, WMTS, WMS等）           | Leaflet, OpenLayers, MapLibre GL JS, Mapbox GL JS | QGIS, gdal2tiles等で生成           |
| 画像オーバーレイ   | 任意画像の地図重ね合わせ                     | Leaflet, OpenLayers, Mapbox GL JS        | QGIS, GDALで座標付与可             |
| Mapbox Style JSON  | 地図スタイル定義                             | MapLibre GL JS, Mapbox GL JS             | Studio, QGISプラグイン等で作成     |

### 3Dデータ形式

[▲目次へ戻る](#目次)

| データ形式         | 概要・用途                                   | 主な対応ライブラリ                       | 備考・変換例                       |
|--------------------|----------------------------------------------|------------------------------------------|------------------------------------|
| 3D Tiles           | 大規模3D地理空間データ配信                   | CesiumJS, deck.gl                        | FME, PLATEAUツール, obj2gltf, entwine等で変換 |
| glTF               | 軽量3Dモデル                                 | CesiumJS, three.js                       | obj2gltf, FBX2glTF, Blender等で変換|
| OBJ/FBX/STL/PLY    | 汎用3Dモデル                                 | three.js                                 | Blender, MeshLab, obj2gltf等で変換 |
| LAS/LAZ            | 点群データ                                   | deck.gl, Potree, CesiumJS（3D Tiles変換）| PotreeConverter, entwine, FME等で変換|
| CityGML            | 都市モデルXML                                | CesiumJS（3D Tiles変換）, FME            | FME, PLATEAUツール等で3D Tiles変換 |
| CZML               | 時系列3D地理データ                           | CesiumJS                                 |                                    |
| DEM                | 標高・地形ラスタデータ                       | CesiumJS, Mapbox GL JS                   | GDAL, QGISで生成・変換              |

### データ形式変換・生成に役立つ主なツール・ライブラリ

[▲目次へ戻る](#目次)

| ツール・ライブラリ      | 主な用途・特徴                                         | 公式・参考リンク                                         |
|------------------------|------------------------------------------------------|----------------------------------------------------------|
| ogr2ogr                | 多様なGISデータ形式の変換（コマンドライン/ライブラリ） | [GDAL/ogr2ogr公式](https://gdal.org/programs/ogr2ogr.html) |
| QGIS                   | GUIで多様なGISデータ変換・編集                        | [QGIS公式](https://qgis.org/ja/site/)                    |
| FME                    | 複雑な空間データ変換・自動化                          | [FME公式](https://www.safe.com/jp/)                      |
| Blender                | 3Dモデル編集・変換（OBJ, FBX, glTF等）                | [Blender公式](https://www.blender.org/)                  |
| obj2gltf, FBX2glTF     | 3DモデルをglTFへ変換                                  | [obj2gltf](https://github.com/CesiumGS/obj2gltf) / [FBX2glTF](https://github.com/facebookincubator/FBX2glTF) |
| PotreeConverter        | LAS/LAZ等の点群をPotree用形式に変換                   | [PotreeConverter公式](https://github.com/potree/PotreeConverter) |
| entwine                | 点群データを3D Tiles等に変換                          | [entwine公式](https://entwine.io/)                       |
| mapshaper              | GeoJSON/TopoJSON等の変換・簡易編集                    | [mapshaper公式](https://mapshaper.org/)                  |
| tippecanoe             | GeoJSON等からMVT（ベクトルタイル）生成                | [tippecanoe公式](https://github.com/mapbox/tippecanoe)   |
| gdal2tiles             | ラスタ画像からXYZタイル生成                           | [gdal2tiles公式](https://gdal.org/programs/gdal2tiles.html) |
| PLATEAUツール          | CityGML→3D Tiles変換など都市モデル用                  | [PLATEAU公式](https://www.mlit.go.jp/plateau/)           |
| csv2geojson            | CSV→GeoJSON変換                                       | [csv2geojson](https://csv2geojson.org/)                  |

## QGIS・AutoCAD・ArcGIS・BIM/CIMとの連携

[▲目次へ戻る](#目次)

- **QGISとの連携**  
  QGISは多様な地理空間データの編集・変換・可視化が可能なオープンソースGISです。QGISで作成・編集したGeoJSONやシェープファイル、ベクトルタイル（MVT）、ラスタタイル、3Dモデル（CityGML等）は、LeafletやOpenLayers、MapLibre GL JS、CesiumJSなどのWeb地図・3D地図ライブラリで活用できます。QGIS2WebやQGIS2threejsなどのプラグインを使えば、QGISのプロジェクトをそのままWeb用にエクスポートすることも容易です。QGISはデータ形式変換のハブとしても非常に有用です。

- **AutoCADとの連携**  
  AutoCAD（DWG/DXF形式）は建築・土木設計で広く使われており、**AutoCAD 2013形式（DWG/DXF 2013）**で保存されたファイルはQGISやFME、ogr2ogrなど多くのGISツールで安定して読み書き・変換が可能です。  
  特にQGISではAutoCAD 2013形式のDWG/DXFのインポート・エクスポートの再現性が高く、属性情報やジオメトリも正確に取り扱えることが[公式ドキュメントや多くの事例](https://docs.qgis.org/latest/ja/docs/user_manual/working_with_vector/supported_data.html#autocad-dwg-dxf)で確認されています。  
  また、AutoCAD Civil 3DやInfraWorksなどBIM/CIM対応製品からLandXMLやIFC、3Dモデルデータをエクスポートし、Web可視化に活用する事例もあります。

- **ArcGISとの連携**  
  ArcGISはESRI社の商用GISで、Shapefile、FileGDB、GeoJSON、KML、CSV、3D Tiles、Scene Layer Package（SLPK）、LAS/LAZなど多様なデータ形式の入出力・変換が可能です。ArcGIS ProやArcGIS OnlineからGeoJSONや3D Tiles、glTF等にエクスポートし、Web地図・3D地図ライブラリで利用できます。ArcGIS API for JavaScriptもWeb地図開発に利用されますが、他のOSSライブラリとのデータ連携も容易です。  
  また、**ArcGISはAutoCADとの連携強化も進めており**、ArcGIS ProではDWG/DXFファイル（AutoCAD 2013形式を含む複数バージョン）を直接読み込み・編集できます。ArcGISはAutoCAD 2013形式以外（2000/2004/2007/2010/2013/2018等）にも幅広く対応しており、[公式ドキュメント](https://pro.arcgis.com/ja/pro-app/latest/help/data/cad/supported-cad-formats.htm)でもサポートバージョンが明記されています。AutoCAD Map 3DやCivil 3Dとのデータ交換（属性・座標系の保持）もサポートされており、ArcGIS for AutoCADアドインを利用することで、AutoCAD上でArcGISの地理情報やサービスを直接利用・編集することも可能です。これにより、CADとGIS間のデータ連携・ワークフローの再現性や効率が大きく向上しています。

- **BIM/CIMとの連携**  
  BIM（Building Information Modeling）やCIM（Construction Information Modeling）で作成されたIFC、CityGML、glTF、3D Tiles、LAS/LAZ等の3Dモデル・点群データは、Web地図・3D地図ライブラリでの可視化・共有が進んでいます。特にCesiumJSやthree.js、deck.gl、Potreeなどは大規模な3D都市モデルや点群データのWeb可視化に強みがあります。QGISやFME、PLATEAUツール、Blender等を活用して、BIM/CIMデータをWeb向けの形式（glTF, 3D Tiles, GeoJSON等）に変換し、WebGISやWeb3Dビューアでの活用が広がっています。

## 3D・VR・AR・MRとの関係

[▲目次へ戻る](#目次)

- **3D地図とVR（バーチャルリアリティ）**
  - CesiumJSやthree.jsなどのWebGLベースの3D地図ライブラリは、WebVR/WebXR APIと組み合わせることで、VRゴーグル（Oculus, HTC Vive等）での3D都市モデルや地形の没入型体験が可能です。
  - 3D TilesやglTF形式の都市モデル・BIMデータをVR空間で閲覧・操作する事例も増えています。

- **3D地図とAR（拡張現実）**
  - WebAR（WebXR API, AR.js, 8th Wall等）とthree.jsやMapbox GL JSを組み合わせることで、スマートフォンやタブレットのカメラ映像上に地図や3Dモデルを重ねて表示するARアプリが開発できます。
  - CesiumJSやMapboxの一部機能もAR対応の実証例があります。

- **3D地図とMR（複合現実）**
  - MR（Mixed Reality）はVRとARの融合で、現実空間と仮想地図・3Dモデルを高度に重ね合わせて操作可能です。
  - HoloLens等のMRデバイス向けに、three.jsやCesiumJS、Unity+WebView等を活用した都市モデル・BIMデータのMR可視化も研究・実用化が進んでいます。

- **データ形式のポイント**
  - VR/AR/MRでの3D地図・都市モデル活用には、glTFや3D Tiles、GeoJSON、点群（LAS/LAZ）などWeb標準の軽量3Dフォーマットが推奨されます。
  - WebXR APIやA-Frame、Babylon.jsなどのフレームワークと連携することで、Web地図ライブラリの3DデータをVR/AR/MR体験に活用できます。

## 代表的なサービス・アプリと3D・VR・AR・MRとの関係

[▲目次へ戻る](#目次)

| サービス・アプリ名                | 主な利用ライブラリ         | 概要・特徴                                                                 | 3D/VR/AR/MR対応           |
|-----------------------------------|---------------------------|----------------------------------------------------------------------------|---------------------------|
| Google Maps                       | Google Maps JS API        | 世界最大級の地図サービス。2D/3D地図、ストリートビュー、ルート検索等。         | 3D地図（Web/モバイル）、一部AR（Live View）|
| Mapbox                            | Mapbox GL JS, deck.gl     | カスタム地図・3D地図・ナビゲーションAPI。多くのWeb/モバイルアプリで採用。     | 3D地図、AR（Mapbox Vision）|
| PLATEAU VIEW                      | CesiumJS                  | 国土交通省PLATEAUの3D都市モデルWebビューア。                                 | 3D都市モデル、WebGL        |
| Cesium Stories                    | CesiumJS                  | 3D地球上でストーリーやデータを可視化・共有できるWebサービス。                 | 3D地球、WebGL              |
| ArcGIS Online/Scene Viewer        | ArcGIS JS API, CesiumJS   | ESRIのクラウドGIS。2D/3D地図、都市モデル、点群、VR/AR/MR連携も可能。          | 3D地図、VR/AR/MR（一部対応）|
| OpenStreetMap 3D                  | OSM Buildings, three.js   | OSMデータを使った3D都市モデルWeb表示。                                      | 3D地図                     |
| QGIS2threejs出力例                | three.js                  | QGISから出力した3D地形・都市モデルのWeb可視化。                              | 3D地図                     |
| Potree Viewer                     | Potree                    | 大規模点群データのWeb可視化。                                               | 3D点群                     |
| Babylon.js Playground             | Babylon.js                | WebGLベースの3D/VR/AR/MRデモ・サンプル集。                                   | 3D/VR/AR/MR                |
| Mapillary                         | Mapbox GL JS, three.js    | ストリートビュー画像の共有・解析サービス。3D点群やAR機能も一部提供。           | 3D点群、AR                  |
| PLATEAU x XR                      | CesiumJS, Unity           | PLATEAU都市モデルのVR/AR/MR体験・実証プロジェクト。                           | VR/AR/MR                    |
| [KOLC+](https://www.kolcplus.jp/) | CesiumJS, MapLibre GL JS  | 国土地理院の3D都市モデル・地理空間情報統合ビューア。PLATEAUや地理院地図、点群、地形、各種オープンデータをWebで統合表示。 | 3D都市モデル、点群、WebGL、今後XR連携も検討中 |
| [PLATEAU SDK for Unity](https://sdk.plateau.reearth.io/) | Unity, Cesium for Unity   | PLATEAU都市モデルをUnityで活用・VR/AR/MRアプリ開発が可能なSDK。               | VR/AR/MR                    |
| [Re:Earth](https://reearth.io/)   | CesiumJS, MapLibre GL JS  | オープンソースの3D地理空間プラットフォーム。PLATEAUや各種地理空間データの可視化・共有。 | 3D都市モデル、WebGL         |

- これらのサービス・アプリは、WebGLベースの地図・3D可視化ライブラリを活用し、3D都市モデルや点群、ストリートビュー、ナビゲーション、VR/AR/MR体験など多様な地理空間情報サービスを実現しています。
- 特にCesiumJS、three.js、Babylon.js、deck.gl、Mapbox GL JSなどは、3D地図や都市モデルのWeb可視化・共有・インタラクション・VR/AR/MR連携の基盤として広く利用されています。