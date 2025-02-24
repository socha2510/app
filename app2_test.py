import unittest
import os
import pandas as pd
from app2 import load_data, create_dataframe, file_paths

class TestAppFunctions(unittest.TestCase):

    def test_load_data(self):
        """
        file_pathsリストから1つファイルを選び、load_dataをテスト。
        JSONの中身が想定構造になっているか確認。
        """
        file_path = file_paths[0]
        # ファイルが存在するか
        self.assertTrue(os.path.exists(file_path), f"{file_path} does not exist")

        # load_dataが返却する型をチェック
        data = load_data(file_path)
        self.assertIsInstance(data, list, "JSONを読み込んだ結果が 'list' ではありません。")

        if data:
            self.assertIsInstance(data[0], dict, "JSONの各要素は dict を想定しています。")

    def test_create_dataframe(self):
        """
        create_dataframe で DataFrame が結合されるかチェック。
        """
        df = create_dataframe()
        # DataFrameかどうか
        self.assertIsInstance(df, pd.DataFrame, "返却オブジェクトが DataFrame ではありません。")
        # 行数が 0ではない
        self.assertGreater(len(df), 0, "作成されたDataFrameが空です。")

        # 期待するカラムが含まれているか (例として 'id', 'title', 'content' など)
        required_cols = {'id', 'title', 'content'}
        self.assertTrue(
            required_cols.issubset(df.columns),
            f"DataFrameに必要なカラム {required_cols} が含まれていません。"
        )

    def test_s23_json_content(self):
        """
        s23.json の内容を具体的にチェックするテストケース。
        unittestで「id=1」の最初の要素が期待したタイトル等を持つかなど確認。
        """
        file_path = 's23.json'
        self.assertTrue(os.path.exists(file_path), f"{file_path} does not exist")

        data = load_data(file_path)
        self.assertIsInstance(data, list, "s23.json がリスト形式で構成されていません。")

        # 少なくとも先頭に1件はある想定
        self.assertGreater(len(data), 0, "s23.json が空です。")

        # 先頭要素を確認
        first_item = data[0]
        # 例として、キーが 'id' や 'title' 'content' などを含んでいるか確認
        expected_keys = {'link', 'id', 'code', 'title', 'group', 'date', 'content'}
        self.assertTrue(
            expected_keys.issubset(first_item.keys()),
            f"s23.jsonの先頭要素に必要なキー {expected_keys} が見つかりません。"
        )

        # 具体的な値をテスト (一部抜粋)
        # ※ userが表示してくれた JSON の冒頭によると、id=1, title="一年は組の新学期の段" などが書かれている。
        self.assertEqual(first_item['id'], 1, "先頭要素の id が 1 ではありません。")
        self.assertEqual(first_item['title'], "一年は組の新学期の段", "先頭要素のタイトルが想定と異なります。")
        self.assertEqual(first_item['link'], True, "先頭要素の 'link' が True ではありません。")


if __name__ == '__main__':
    unittest.main()
