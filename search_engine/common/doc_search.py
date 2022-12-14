import asyncio
import sys

import pymongo


from operator import itemgetter

from search_engine.common.cosine_similarity import CosineSimilarity
from search_engine.common.common_tools import gen_stop_words, text_seg
from search_engine.database.motor_base import MotorBase
from search_engine.utils.log import logger

stop_words = gen_stop_words()


async def doc_search(*, query: str, mongo_db=None) -> list:
    """
    Elastic search
    :param query:
    :return:
    """
    result = []
    try:
        if mongo_db is None:
            mongo_db = MotorBase().get_db()
        seg_query = text_seg(text=query, stop_words=stop_words)
        query_list, word_id_list, doc_id_list, final_query_list = [], [], [], []

        for each_word in seg_query:
            query_list.append({
                'word': each_word
            })

        # 分词的词组转化成单词id 单词id最好加载到内存中 节省一次数据库查询
        word_cursor = mongo_db.word_id.find(
            {"$or": query_list},
            {'word_id': 1, '_id': 0}
        )

        async for word in word_cursor:
            word_id_list.append(word)

        # 根据单词id找出文档
        index_cursor = mongo_db.inverted_index.find(
            {"$or": word_id_list},
            {'inverted_list': 1, 'word_tf': 1, '_id': 0}
        )

        async for index in index_cursor:
            cur_doc_id = 0
            # 将倒排列表数据加载进内存
            for i in index['inverted_list']:
                cur_doc_id += i[0]
                doc_id_list.append(cur_doc_id)
        print(doc_id_list)
        # 根据文档id 找出文档详细信息
        for each_doc in set(doc_id_list):
            final_query_list.append({
                'doc_id': each_doc
            })

        doc_cursor = mongo_db.doc_id.find(
            {"$or": final_query_list},
            {"_id": 0}
        )

        # async for doc in doc_cursor:
        #     result.append(doc)

        # query_list = text_seg(query)
        async for doc in doc_cursor:
            # 对输出的结果计算余弦相似度
            doc_data = {
                'index': doc['title'],
                'value': text_seg(doc['title'].lower())
            }
            cos = CosineSimilarity(seg_query, doc_data)
            vector = cos.create_vector()
            cs_res = cos.calculate(vector)
            doc['cs_value'] = cs_res['value']
            result.append(doc)

    except pymongo.errors.OperationFailure as e:
        logger.error(e)

    except Exception as e:
        logger.error(e)

    # return result

    result_sorted = sorted(
        [x for x in result if x['cs_value']>=0.15],
        reverse=True,
        key=itemgetter('cs_value'))

    return result_sorted



if __name__ == '__main__':
    res = asyncio.get_event_loop().run_until_complete(doc_search(query='Advanced Python Programming'))
    for each in res:
        print(each['title'])
        print(each['cs_value'])