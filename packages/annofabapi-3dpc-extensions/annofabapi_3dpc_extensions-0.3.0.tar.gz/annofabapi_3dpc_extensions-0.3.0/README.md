# annofabapi-3dpc-extensions
[![Build Status](https://app.travis-ci.com/kurusugawa-computer/annofabapi-3dpc-extensions.svg?branch=main)](https://app.travis-ci.com/kurusugawa-computer/annofabapi-3dpc-extensions)
[![PyPI version](https://badge.fury.io/py/annofabapi-3dpc-extensions.svg)](https://badge.fury.io/py/annofabapi-3dpc-extensions)
[![Python Versions](https://img.shields.io/pypi/pyversions/annofabapi-3dpc-extensions.svg)](https://pypi.org/project/annofabapi-3dpc-extensions/)
[![Documentation Status](https://readthedocs.org/projects/annofabapi-3dpc-extensions/badge/?version=latest)](https://annofabapi-3dpc-extensions.readthedocs.io/en/latest/?badge=latest)



[annofabapi](https://github.com/kurusugawa-computer/annofab-api-python-client)の3次元アノテーション用の拡張機能です。

# Install

* Python 3.9+

# Install

```
$ pip install annofabapi-3dpc-extensions
```


# Usage

cuboidアノテーションやセグメントアノテーションに対応したデータクラスを利用できます。

```python
from annofabapi.parser import SimpleAnnotationDirParser

from annofab_3dpc.annotation import (
    CuboidAnnotationDetailDataV2,
    EulerAnglesZXY,
    SegmentAnnotationDetailData,
    SegmentData,
    convert_annotation_detail_data,
)

parser = SimpleAnnotationDirParser("tests/data/task1/input1.json")
result = parser.parse(convert_annotation_detail_data)

segment_annotation_data = result.details[0].data
cuboid_annotation_data = result.details[1].data
assert type(segment_annotation_data) == SegmentAnnotationDetailData
assert type(cuboid_annotation_data) == CuboidAnnotationDetailDataV2


### cuboid annotation

print(cuboid_annotation_data)
# => CuboidAnnotationDetailDataV2(shape=CuboidShapeV2(dimensions=Size(width=6.853874863204751, height=0.2929844409227371, depth=4.092537841193188), location=Location(x=-11.896872014598989, y=-3.0571381239812996, z=0.3601047024130821), rotation=EulerAnglesZXY(x=0, y=0, z=0), direction=CuboidDirection(front=Vector3(x=1, y=0, z=0), up=Vector3(x=0, y=0, z=1))), kind='CUBOID', version='2')

# オイラー角をクォータニオンに変換
print(cuboid_annotation_data.shape.rotation.to_quaternion())
# => [1.0, 0.0, 0.0, 0.0]

# クォータニオンからオイラー角に変換
print(EulerAnglesZXY.from([1.0, 0.0, 0.0, 0.0]))
# => EulerAnglesZXY(x=-0.0, y=0.0, z=0.0)


### segment annotation
print(segment_annotation_data)
# => SegmentAnnotationDetailData(data_uri='./input1/7ba51c15-f07a-4e29-8584-a4eaf3a6812a')

# セグメント情報が格納されたファイルを読み込む
with parser.open_outer_file(Path(segment_annotation_data.data_uri).name) as f:
    dict_segmenta_data = json.load(f)
    segment_data = SegmentData.from_dict(dict_segmenta_data)
    assert type(segment_data) == SegmentData
    assert len(segment_data.points) > 0
    print(segment_data.points)
    # => [130439, 130442, ... ]

```


# 開発者向けドキュメント

https://github.com/kurusugawa-computer/annofabapi-3dpc-extensions/blob/main/README_for_developer.md 参照
