# 野外空間early warning：2026-10-08時点のデータ実行可能性と結論境界

## 現在の結論

**Love & Otto (2026) の inter-individual distance CV（`CV_ind`、`CV_pop`、比）が、野外個体群の将来の人口動態を追加的に予測するか、という問いはまだ決着していない。** これは「検出力がない」と判明したからではなく、GPSと将来アウトカムを同時に満たすデータの不足が主な理由である。

Love & Otto の論文が直接検証したのは spatial change / cohesion state の検出であり、later demography の時系列holdoutとは区別する。

## 実際に決着したこと

| 系 | 実行した内容 | 判定 |
|---|---|---|
| **Ya Ha Tinda elk / 予測主解析** | 公式Movebank 1,585,456測位をソースハッシュ付きで監査。n≥10の日を30日以上満たす秋は8年、凍結Dryad将来繁殖データと重なるのは6年 | **STOP：6/11年。人口動態モデル0件** |
| **Ya Ha Tinda / GPS測定安定性** | 474適格日・8年。10頭パネル選択を繰り返し、全装着個体利用との違いを確認 | **実測の観測依存性**：パネル内中央値SD 0.0993、隣接日の変化方向不一致39.1%。後年の生存・繁殖は未評価 |
| **Mac Hugh caribou** | ルート経度分散を加えた1年先のrecruitment予測、16年分の前向き時系列holdout | **追加利得なし**：baseline RMSE 13.309、経度分散追加RMSE 13.815。ただしLove–OttoのIID指標ではない |
| **Mac Hugh / 別RSFファイル** | 公式106 MB sourceの列名だけを確認。年・環境12列にID、時計時刻、座標なし | **schema STOP**：このファイル単体では同時刻のIIDを再構成できない |
| **Bathurst caribou** | GPS公開範囲と年次recruitment資料の確認 | **HOLD**：Movebank catalogueはsummary公開で位置イベント公開を未確認。調査年の欠落・群れ混合もある |
| **Central Arctic Herd** | 先行論文の個体GPS・翌年reproduction/survivalの設計確認 | **HOLD**：有望な自然historyだが、GPSは州法に基づき非公開 |

## 強いポイント：Ya Ha Tinda のSTOPは推定ではなく公式rawで観測した

本来のsourceは `10.5441/001/1.5g4h5t6c`。原本CSVのSHA256は
`1069cd7531d1d7a519cb817b09d015be91c552ecafab504869a81eb01eff4201`。
ロック済み条件を変えず、秋季（9/15–11/15）の正午±6.5時間以内に10頭以上を把握した日が30日以上ある年は

`2004, 2013, 2014, 2015, 2016, 2017, 2018, 2019`。

翌冬calf:cowを予測できる源泉の最終年が2018なので、解析可能な秋は

`2004, 2013, 2014, 2015, 2016, 2017`

の6年。事前固定した11年未満のため、**正しく停止**した。

研究者による教材用CSV（138,433測位、2001–2005年）は部分抽出で、現在の全期間sourceには代用しない。また、移動データだけの8年を、人口動態について8独立年あるかのように扱わない。

## Love–Otto方法論への新しい実測的示唆

公式GPSから同じ日に10頭を選び直すだけで、比 `CV_ind/CV_pop` が変わる。474適格日のうち460日は10頭以上の選択余地があり、**10頭パネルの構成による推定差**が存在した。隣接日の平均CV変化方向も「固定10頭選択」と「利用可能な全首輪個体」で39.1%食い違った。

これは**将来人口動態を予測できない**ことの証拠ではない。むしろ「現時点の空間配置が正確に測れているか」という前段階の問題である。

- 全装着個体の空間配置も、群れ全体のground truthではない。
- 日ごとに測位時刻がずれ、受け入れた同日位置の中央値spreadは6.03時間である。
- 10頭標本の異なる反復抽出を、独立した野生個体群や独立年として数えない。
- 2026年の既存sampling-design文献が一般的なcollar sample biasを扱うので、測定感度が一般に「初発見」とは主張しない。

## 次の候補を通すための条件

新規候補に必要なのは、**同じ集団の同じ期間で、同時刻に近い個体座標と後続人口動態を測定し、時点tの指標を固定したうえで未来t+hをholdoutすること**。

順番は以下で固定する。

1. 元データへの合法的なアクセスと利用条件を確認する。
2. 対象群・繁殖アウトカム・GPSの年月をそれぞれ確認し、共通calendarの十分な反復があるか**アウトカム値に触れる前に**確定する。
3. 同時位置の定義、個体数・観測日数、指標の固定を行う。
4. baseline（現在の人口動態・range・effort・season）を超えるfuture predictionを未使用年または未使用集団で比較する。
5. イベントと非イベントのfull denominator、校正、観測panelの不確実性を記録する。

Ya Ha Tindaの最低11年ルールは**その実験固有**であり、他研究へ自動流用しない。

## 独立した近縁研究

Mac Hugh et al. (2026) はlongitude varianceという別の測度で、16年のforward forecastで追加予測利得がなかった。ただし同時刻の個体間距離が必要なLove–Otto指標は算出していない。これは**野外の空間proxy一般の反証ではない**。

Bathurstの公開GPS一覧は「summary」可視性で、raw位置への許可を保証しない。late-winter calf:cowも一部年度は隣接 herd との混合で推定できていない。

Central Arctic Herd の個体GPSは研究利用されているが、元論文が非公開と明示している。URLを知っていることはデータ利用権を持つことではない。

## ソース・再現性

- Love & Otto (2026), *Methods in Ecology and Evolution*, DOI `10.1111/2041-210x.70375`.
- Ya Ha Tinda original source: DOI `10.5441/001/1.5g4h5t6c`, `artifacts/yht_spatial_warning/official_movebank_coverage_overlap_stop.json`.
- Ya Ha Tinda sample reliability: `artifacts/yht_spatial_warning/official_panel_sensitivity_result.json`.
- Mac Hugh (2026): DOI `10.1002/ecs2.70553`, official data DOI `10.5683/SP3/0ROESU`, `artifacts/mac_hugh_recruitment/temporal_result_locked.json`.
- GNWT catalogue: https://www.movebank.org/cms/movebank-content/room2roam-archive
- Bathurst calf:cow report: https://www.gov.nt.ca/ecc/sites/ecc/files/resources/308_manuscript_0.pdf
- Central Arctic Herd: https://doi.org/10.3389/fevo.2022.899585

この資料はソースの実行可能性と主張の上限を管理するもの。NEE finite closure の自然界での検証成功を宣言しない。
