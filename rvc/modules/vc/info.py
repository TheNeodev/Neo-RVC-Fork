import traceback
from i18n.i18n import I18nAuto
from datetime import datetime
import torch

from .hash import model_hash_ckpt, hash_id, hash_similarity

i18n = I18nAuto()


def show_model_info(cpt, show_long_id=False):
    try:
        h = model_hash_ckpt(cpt)
        id = hash_id(h)
        idread = cpt.get("id", "None")
        hread = cpt.get("hash", "None")
        if id != idread:
            id += (
                "("
                + i18n("实际计算")
                + "), "
                + idread
                + "("
                + i18n("从模型中读取")
                + ")"
            )
        sim = hash_similarity(h, hread)
        if not isinstance(sim, str):
            sim = "%.2f%%" % (sim * 100)
        if not show_long_id:
            h = i18n("不显示")
            if h != hread:
                h = i18n("相似度") + " " + sim + " -> " + h
        elif h != hread:
            h = (
                i18n("相似度")
                + " "
                + sim
                + " -> "
                + h
                + "("
                + i18n("实际计算")
                + "), "
                + hread
                + "("
                + i18n("从模型中读取")
                + ")"
            )
        txt = f"""{i18n("模型名")}: %s
{i18n("封装时间")}: %s
{i18n("模型作者")}: %s
{i18n("信息")}: %s
{i18n("采样率")}: %s
{i18n("音高引导(f0)")}: %s
{i18n("版本")}: %s
{i18n("ID(短)")}: %s
{i18n("ID(长)")}: %s""" % (
            cpt.get("name", i18n("Unknown")),
            datetime.fromtimestamp(float(cpt.get("timestamp", 0))),
            cpt.get("author", i18n("Unknown")),
            cpt.get("info", i18n("None")),
            cpt.get("sr", i18n("Unknown")),
            i18n("有") if cpt.get("f0", 0) == 1 else i18n("无"),
            cpt.get("version", i18n("None")),
            id,
            h,
        )
    except:
        txt = traceback.format_exc()

    return txt


def show_info(path):
    try:
        if hasattr(path, "name"):
            path = path.name
        a = torch.load(path, map_location="cpu")
        txt = show_model_info(a, show_long_id=True)
        del a
    except:
        txt = traceback.format_exc()

    return txt
