"""Customize Simple node parser."""
import json
from typing import Any, Callable, List, Optional, Sequence
from bisect import bisect_right
from pathlib import Path

from llama_index.core.bridge.pydantic import Field
from llama_index.core.callbacks import CallbackManager
from llama_index.core.node_parser import NodeParser
from llama_index.core.node_parser.node_utils import build_nodes_from_splits
from llama_index.core.node_parser.text.utils import split_by_sentence_tokenizer
from llama_index.core.schema import BaseNode, MetadataMode
from llama_index.core import Document
from llama_index.core.utils import get_tqdm_iterable

DEFAULT_WINDOW_SIZE = 3
DEFAULT_WINDOW_METADATA_KEY = "window"
DEFAULT_OG_TEXT_METADATA_KEY = "original_text"



class LawsSentenceWindowNodeParser(NodeParser):
    sentence_splitter: Callable[[str], List[str]] = Field(
        default_factory=split_by_sentence_tokenizer,
        description="The text splitter to use when splitting documents.",
        exclude=True,
    )
    window_size: int = Field(
        default=DEFAULT_WINDOW_SIZE,
        description="The number of sentences on each side of a sentence to capture.",
        gt=0,
    )
    window_metadata_key: str = Field(
        default=DEFAULT_WINDOW_METADATA_KEY,
        description="The metadata key to store the sentence window under.",
    )
    original_text_metadata_key: str = Field(
        default=DEFAULT_OG_TEXT_METADATA_KEY,
        description="The metadata key to store the original sentence in.",
    )

    @classmethod
    def class_name(cls) -> str:
        return "LawsSentenceWindowNodeParser"

    @classmethod
    def laws_name(cls, path):
        #刑事司法协助
        _mapping["zhonghuarenmingongguojixingshisifaxiezhufa.txt"] = "中华人民共和国刑事司法协助法"
        _mapping["zhonghuarenmingongheguoheaerjiliyaminzhurenmingongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和阿尔及利亚人民民主共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguoheagentinggongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和阿根廷共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguoheaishaniyagongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和阿塞拜疆共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohealaboaijigongheguoguanyuminshishangshihexingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和阿拉伯埃及共和国关于民事、商事和刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohealabolianheqiuzhangguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和阿拉伯联合酋长国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguoheaodaliyaguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和澳大利亚关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohebabaduosiguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和巴巴多斯关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohebaieluosigongheguoguanyuminshihexingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和白俄罗斯共和国关于民事和刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohebajisitanyisilangongheguozhnegfuguanyuxingshisifaxiezhudexieding.txt"] = "中华人民共和国和巴基斯坦伊斯兰共和国政府关于刑事司法协助的协定"
        _mapping["zhonghuarenmingongheguohebaojialiyagongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和保加利亚共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohebaxilianbanggongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和巴西联邦共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohebilishiwangguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和比利时王国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohebolanrenmingongheguoguanyuminshihexingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和波兰人民共和国关于民事和刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohebosiniyaheheisaigeweinaguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和波斯尼亚和黑塞哥维那关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohechaoxianminzhuzhuyirenmingongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和朝鲜民主主义人民共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohedabuliedianjibeiaierlanlianhewangguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和大不列颠及北爱尔兰联合王国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohedahanminguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和大韩民国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguoheeluosilianbangguanyuminshihexingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和俄罗斯联邦关于民事和刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohefeilvbingongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和菲律宾共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohegangguogongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和刚果共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohegelinnadaguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和格林纳达关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohegelunbiyagongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和哥伦比亚共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohegubagongheguoguanyuminshihexingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和古巴共和国关于民事和刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohegukelanguanyuminshihexingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和哈萨克斯坦共和国关于民事和刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohehasakesitangongheguoguanyuminshihexingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和哈萨克斯坦共和国关于民事和刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohejianadaguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和加拿大关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohejierjisigongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和吉尔吉斯共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohelaoworenminminzhugongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和老挝人民民主共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohelatuoweiyagongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和拉脱维亚共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohelitaowangongheguoguanyuminshihexingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和立陶宛共和国关于民事和刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguoheluomaniyaguanyuminshihexingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和罗马尼亚关于民事和刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohemaertaguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和马尔他关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohemeilijianhezhongguozhengfuguanyuxingshisifaxiezhudexieding.txt"] = "中华人民共和国和美利坚合众国政府关于刑事司法协助的协定"
        _mapping["zhonghuarenmingongheguohemenggurenmingongheguoguanyuminshihexingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和蒙古人民共和国关于民事和刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohemilugongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和秘鲁共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohemoxigehezhongguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和墨西哥合众国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohenamibiyagongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和纳米比亚共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohenanfeigongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和南非共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohenimeiniyagongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和尼日利亚联邦共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguoheputaoyagongheguoguanyuxingshisifaxiezhudexieding.txt"] = "中华人民共和国和葡萄牙共和国关于刑事司法协助的协定"
        _mapping["zhonghuarenmingongheguoheribenguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和日本国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohesaipulusigongheguoguanyuminshishangshihexingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和塞浦路斯共和国关于民事、商事和刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohesililankaminzhushehuizhuyigongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和斯里兰卡民主社会主义共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohetaiwangguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和泰王国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohetajikesitangongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和塔吉克斯坦共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohetuerqigonghegguanyuminshishangshihexingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和土耳其共和国关于民事、商事和刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohetunisigongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和突尼斯共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguoheweineiruilaboliwaerhongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和委内瑞拉玻利瓦尔共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohewuzibiekesitangongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和乌兹别克斯坦共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohexibanyawangguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和西班牙王国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohexilagongheguoguanyuminshihexingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和希腊共和国关于民事和刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguohexinxilanguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和新加坡关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguoheyidaligongheguozhengfuguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和意大利共和国政府关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguoheyilanyisilangongheguogunguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和伊朗伊斯兰共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguoheyindunixiyagongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和印度尼西亚共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguoheyuenanshehuizhuyigongheguoguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国和越南社会主义共和国关于刑事司法协助的条约"
        _mapping["zhonghuarenmingongheguozhengfuhefalanxigongheguozhengfuguanyuxingshisifaxiezhudexieding.txt"] = "中华人民共和国政府和法兰西共和国政府关于刑事司法协助的协定"
        _mapping["zhonghuarenmingongheguozhengfuhemalaixiyazhengfuguanyuxingshisifaxiezhudetiaoyue.txt"] = "中华人民共和国政府和马来西亚政府关于刑事司法协助的条约"
        ##移交
        _mapping["zhonghuarenmingongheguoheaodaliyaguanyuyiguanbeipanxingrendetiaoyue.txt"] = "中华人民共和国和澳大利亚关于移交被判刑人的条约"
        _mapping["zhonghuarenmingongheguoheasaibaijianggongheguoguanyuyiguanbeipanxingrendetiaoyue.txt"] = "中华人民共和国和阿塞拜疆共和国关于移交被判刑人的条约"
        _mapping["zhonghuarenmingongheguohebajisitanyisilangongheguoguanyuyiguanbeipanxingrendetiaoyue.txt"] = "中华人民共和国和巴基斯坦伊斯兰共和国关于移交被判刑人的条约"
        _mapping["zhonghuarenmingongheguohebilishiwangguoguanyuyiguanbeipanxingrendetiaoyue.txt"] = "中华人民共和国和比利时王国关于移交被判刑人的条约"
        _mapping["zhonghuarenmingongheguohedahanminguoguanyuyiguanbeipanxingrendetiaoyue.txt"] = "中华人民共和国和大韩民国关于移交被判刑人的条约"
        _mapping["zhonghuarenmingongheguoheeluosilianbangguanyuyiguanbeipanxingrendetiaoyue.txt"] = "中华人民共和国和俄罗斯联邦关于移交被判刑人的条约"
        _mapping["zhonghuarenmingongheguohehasakesitangongheguoguanyuyiguanbeipanxingrendetiaoyue.txt"] = "中华人民共和国和哈萨克斯坦共和国关于移交被判刑人的条约"
        _mapping["zhonghuarenmingongheguohejierjisigongheguoguanyuyiguanbeipanxingrendetiaoyue.txt"] = "中华人民共和国和吉尔吉斯共和国关于移交被判刑人的条约"
        _mapping["zhonghuarenmingongheguohemengguguoguanyuyiguanbeipanxingrendetiaoyue.txt"] = "中华人民共和国和蒙古国关于移交被判刑人的条约"
        _mapping["zhonghuarenmingongheguoheputaoyagongheguoguanyuyiguanbeipanxingrendetiaoyue.txt"] = "中华人民共和国和葡萄牙共和国关于移交被判刑人的条约"
        _mapping["zhonghuarenmingongheguohetaiwangguoguanyuyiguanbeipanxingrendetiaoyue.txt"] = "中华人民共和国和泰王国关于移交被判刑人的条约"
        _mapping["zhonghuarenmingongheguohetajikesitangongheguoguanyuyiguanbeipanxingrendetiaoyue.txt"] = "中华人民共和国和塔吉克斯坦共和国关于移交被判刑人的条约"
        _mapping["zhonghuarenmingongheguohewukelanguanyuyiguanbeipanxingrendetiaoyue.txt"] = "中华人民共和国和乌克兰关于移交被判刑人的条约"
        _mapping["zhonghuarenmingongheguohexibanyawangguoguanyuyiguanbeipanxingrendetiaoyue.txt"] = "中华人民共和国和西班牙王国关于移交被判刑人的条约"
        _mapping["zhonghuarenmingongheguoheyilanyisilangongheguoguanyuyiguanbeipanxingrendetiaoyue.txt"] = "中华人民共和国和伊朗伊斯兰共和国关于移交被判刑人的条约"
        ##武器
        _mapping["minbingwuqizhuangbeiguanglitiaoli.txt"] = "民兵武器装备管理条例"
        _mapping["wuqizhuangbeikeyanshengchanxukeguanlitiaoli.txt"] = "武器装备科研生产许可管理条例"
        _mapping["wuqizhuangbeizhiliangguanglitiaoli.txt"] = "武器装备质量管理条例"
        _mapping["zhonghuarenmingongheguorenminjinchashiyongjinxiehewuqitiaoli.txt"] = "中华人民共和国人民警察使用警械和武器条例"
        ##引渡
        _mapping["zhonghuarenmingongheguoheaerjiliyaminzhurenmingongheguoyingdutiaoyue.txt"] = "中华人民共和国与阿尔及利亚人民民主共和国引渡条约"
        _mapping["zhonghuarenmingongheguoheafuhanyisilangongheguoyingdutiaoyue.txt"] = "中华人民共和国与阿富汗伊斯兰共和国引渡条约"
        _mapping["zhonghuarenmingongheguoheaisaiebiyalianbangminzhugongheguo.txt"] = "中华人民共和国与埃塞俄比亚联邦民主共和国条约"
        _mapping["zhonghuarenmingongheguohealabolianheqiuzhangguoyingdutiaoyue.txt"] = "中华人民共和国与阿拉伯联合酋长国引渡条约"
        _mapping["zhonghuarenmingongheguoheangelagongheguoyingdutiaoyue.txt"] = "中华人民共和国与阿根廷共和国引渡条约"
        _mapping["zhonghuarenmingongheguoheasaibaijianggongheguoyingdutiaoyue.txt"] = "中华人民共和国与塞内加尔共和国引渡条约"
        _mapping["zhonghuarenmingongheguohebabaduosiyingdutiaoyuee2m6.txt"] = "中华人民共和国与巴巴多斯引渡条约"
        _mapping["zhonghuarenmingongheguohebaieluosigongheguoyingdutiaoyue.txt"] = "中华人民共和国与白俄罗斯共和国引渡条约"
        _mapping["zhonghuarenmingongheguohebajisitanyisilangongheguoyingdutiaoyue.txt"] = "中华人民共和国与巴基斯坦伊斯兰共和国引渡条约"
        _mapping["zhonghuarenmingongheguohebaojialiyagongheguoyingdutiaoyue.txt"] = "中华人民共和国与保加利亚共和国引渡条约"
        _mapping["zhonghuarenmingongheguohebaxilianbanggongheguoyingdutiaoyue.txt"] = "中华人民共和国与巴西联邦共和国引渡条约"
        _mapping["zhonghuarenmingongheguohebilishiwanguoyingdutiaoyuee2m6.txt"] = "中华人民共和国与比利时王国引渡条约"
        _mapping["zhonghuarenmingongheguohedahanminguoyingdutiaoyue.txt"] = "中华人民共和国与大韩民国引渡条约"
        _mapping["zhonghuarenmingongheguoheeluosilianbangyingdutiaoyue.txt"] = "中华人民共和国与俄罗斯联邦引渡条约"
        _mapping["zhonghuarenmingongheguohefalanxigongheguoyingdutiaoyue.txt"] = "中华人民共和国与法兰西共和国引渡条约"
        _mapping["zhonghuarenmingongheguohefeilvbingongheguoyingdutiaoyue.txt"] = "中华人民共和国与菲律宾共和国引渡条约"
        _mapping["zhonghuarenmingongheguohegangguogongheguoyingdutiaoyuee2m6.txt"] = "中华人民共和国与冈比亚共和国引渡条约"
        _mapping["zhonghuarenmingongheguohegelinnadayindutiaoyuee2m6.txt"] = "中华人民共和国与几内亚共和国引渡条约"
        _mapping["zhonghuarenmingongheguohehasaikesitangongheguoyingdutiaoyue.txt"] = "中华人民共和国与哈萨克斯坦共和国引渡条约"
        _mapping["zhonghuarenmingongheguohejianpuzhaiwangguoyingdutiaoyue.txt"] = "中华人民共和国与柬埔寨王国引渡条约"
        _mapping["zhonghuarenmingongheguohejierjisigongheguoyingdutiaoyue.txt"] = "中华人民共和国与吉尔吉斯共和国引渡条约"
        _mapping["zhonghuarenmingongheguohelaisuotuowangguoyingdutiaoyue.txt"] = "中华人民共和国与老挝人民民主共和国引渡条约"
        _mapping["zhonghuarenmingongheguohelaoworenminminzhugongheguoyingdutiaoyue.txt"] = "中华人民共和国与老挝人民民主共和国引渡条约"
        _mapping["zhonghuarenmingongheguohelitaowangongheguoyingdutiaoyue.txt"] = "中华人民共和国与立陶宛共和国引渡条约"
        _mapping["zhonghuarenmingongheguoheluomaniyayingdutiaoyue.txt"] = "中华人民共和国与罗马尼亚引渡条约"
        _mapping["zhonghuarenmingongheguohemengguguoyingdutiaoyue.txt"] = "中华人民共和国与蒙古国引渡条约"
        _mapping["zhonghuarenmingongheguohemilugongheguoyingdutiaoyue.txt"] = "中华人民共和国与密鲁共和国引渡条约"
        _mapping["zhonghuarenmingongheguohemoxigehezongguoyingdutiaoyue.txt"] = "中华人民共和国与摩西哥合众国引渡条约"
        _mapping["zhonghuarenmingongheguohenamibiyagongheguoyindutiaoyue.txt"] = "中华人民共和国与纳米比亚共和国引渡条约"
        _mapping["zhonghuarenmingongheguohenanfeigongheguoyingdutiaoyue.txt"] = "中华人民共和国与南非共和国引渡条约"
        _mapping["zhonghuarenmingongheguohenosiniyaheheisaigeweinayingdutiaoyue.txt"] = "中华人民共和国与挪威引渡条约"
        _mapping["zhonghuarenmingongheguoheputaoyagongheguoyingdutiaoyue.txt"] = "中华人民共和国与葡萄牙共和国引渡条约"
        _mapping["zhonghuarenmingongheguohesaipulusigongheguoyingdutiaoyuee2m6.txt"] = "中华人民共和国与塞浦路斯共和国引渡条约"
        _mapping["zhonghuarenmingongheguohesililankeminzhushehuizhuyigongheguoyingdutiaoyuee2m6.txt"] = "中华人民共和国与斯里兰卡民主社会主义共和国引渡条约"
        _mapping["zhonghuarenmingongheguohetaiwangguoyingdutiaoyue.txt"] = "中华人民共和国与台湾地区引渡条约"
        _mapping["zhonghuarenmingongheguohetajikesitangongheguoyingdutiaoyuee2m6.txt"] = "中华人民共和国与塔吉克斯坦共和国引渡条约"
        _mapping["zhonghuarenmingongheguohetunisigongheguoyingdutiaoyue.txt"] = "中华人民共和国与突尼斯共和国引渡条约"
        _mapping["zhonghuarenmingongheguohewukelanyingdutiaoyue.txt"] = "中华人民共和国与乌兹别克斯坦引渡条约"
        _mapping["zhonghuarenmingongheguohewuzibiekesitangongheguoyingdutiaoyue.txt"] = "中华人民共和国与乌兹别克斯坦共和国引渡条约"
        _mapping["zhonghuarenmingongheguohexibanyawangguoyingdutiaoyue.txt"] = "中华人民共和国与西班牙王国引渡条约"
        _mapping["zhonghuarenmingongheguoheyidaligongheguoyingdutiaoyue.txt"] = "中华人民共和国与意大利共和国引渡条约"
        _mapping["zhonghuarenmingongheguoheyilangyisilangongheguoyingdutiaoyue.txt"] = "中华人民共和国与伊朗伊斯兰共和国引渡条约"
        _mapping["zhonghuarenmingongheguoheyindufa.txt"] = "中华人民共和国与印度法"
        _mapping["zhonghuarenmingongheguoheyindunixiyagongheguoyingdutiaoyue.txt"] = "中华人民共和国与印度尼西亚共和国引渡条约"
        _mapping["zhonghuarenmingongheguoheyuenanshehuizhuyigongheguoyingdutiaoyuee2m6.txt"] = "中华人民共和国与越南社会主义共和国引渡条约"
        _mapping["zhonghuarenmingongheguohezhiligongheguoyingdutiaoyuee2m6.txt"] = "中华人民共和国与智利共和国引渡条约"
        _mapping["zhonghuarenmingongheguoyumoluogewangguoyingdutiaoyuee2m6.txt"] = "中华人民共和国与摩洛哥王国引渡条约"
        ##


        for name in _mapping:
            if name in path:
                return _mapping[name]
        return "未名"

    @classmethod
    def from_defaults(
        cls,
        sentence_splitter: Optional[Callable[[str], List[str]]] = None,
        window_size: int = DEFAULT_WINDOW_SIZE,
        window_metadata_key: str = DEFAULT_WINDOW_METADATA_KEY,
        original_text_metadata_key: str = DEFAULT_OG_TEXT_METADATA_KEY,
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
        callback_manager: Optional[CallbackManager] = None,
    ) -> "LawsSentenceWindowNodeParser":
        callback_manager = callback_manager or CallbackManager([])

        sentence_splitter = sentence_splitter or split_by_sentence_tokenizer()

        return cls(
            sentence_splitter=sentence_splitter,
            window_size=window_size,
            window_metadata_key=window_metadata_key,
            original_text_metadata_key=original_text_metadata_key,
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel,
            callback_manager=callback_manager,
        )

    def _parse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
        """Parse document into nodes."""
        all_nodes: List[BaseNode] = []
        nodes_with_progress = get_tqdm_iterable(nodes, show_progress, "Parsing nodes")
        for node in nodes_with_progress:
            self.sentence_splitter(node.get_content(metadata_mode=MetadataMode.NONE))
            nodes = self.build_window_nodes_from_documents([node])
            all_nodes.extend(nodes)

        return all_nodes

    def analyze_titles(self, text):
        lines = text.split('\n')
        titles = []
        new_title_keywords = ["条例", "规定", "办法", "决定", "法", "法典"]
        for i, line in enumerate(lines):
            if len(line) > 0 and line[0] != '\n' and line[0] != '\u3000' and line[0] != ' ':
                # 修改标题识别条件
                if not any(keyword in line for keyword in new_title_keywords):
                    continue
                titles.append([line.strip(), i])
        return TitleLocalizer(titles, len(lines))

    def build_window_nodes_from_documents(
        self, documents: Sequence[Document]
    ) -> List[BaseNode]:
        """Build window nodes from documents."""
        all_nodes: List[BaseNode] = []
        for doc in documents:
            text = doc.text
            title_localizer = self.analyze_titles(text)
            lines = text.split('\n')
            nodes = []
            book_name = LawsSentenceWindowNodeParser.book_name(doc.metadata['file_name'])
            for i, line in enumerate(lines):
                if len(line) == 0:
                    continue
                text_splits = self.sentence_splitter(line)
                line_nodes = build_nodes_from_splits(
                    text_splits,
                    doc,
                    id_func=self.id_func,
                )
                title = title_localizer.get_title_line(i)
                if title == None:
                    continue
                for line_node in line_nodes:
                    line_node.metadata["出处"] = f"《{laws_name}·{title[0]}》"
                nodes.extend(line_nodes)
            for i, node in enumerate(nodes):
                window_nodes = nodes[
                    max(0, i - self.window_size) : min(i + self.window_size, len(nodes))
                ]

                node.metadata[self.window_metadata_key] = " ".join(
                    [n.text for n in window_nodes]
                )
                node.metadata[self.original_text_metadata_key] = node.text

                # exclude window metadata from embed and llm
                node.excluded_embed_metadata_keys.extend(
                    [self.window_metadata_key, self.original_text_metadata_key, 'title', 'file_path', '出处', 'file_name', 'filename', 'extension']
                )
                node.excluded_llm_metadata_keys.extend(
                    [self.window_metadata_key, self.original_text_metadata_key, 'file_path', 'file_name', 'filename', 'extension']
                )

                all_nodes.append(node)
        return all_nodes

class TitleLocalizer():
    def __init__(self, titles, total_lines):
        self._titles = titles
        self._total_lines = total_lines 

    def get_title_line(self, line_id):
        indices = [title[1] for title in self._titles] 
        index = bisect_right(indices, line_id)
        if index - 1 < 0:
            return None
        return self._titles[index-1]
        
   
