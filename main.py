"""
main.py
运行整个项目完整的流程管线

Author: Zhu Jiahao
Date: 2025-07-14
"""

import os
from src.api.image_api import OpenCVImageClient
from src.api.qwen_api import QwenClient
from src.api.writing_api import RobotWritingClient
from src.utils.utils import read_txt_file
from src.utils.config import __config__
from src.utils.logger import __logger__

def main():
    """
    @TODO: Describe the whole pipeline
    """
    pipeline_logger = __logger__.get_module_logger("pipeline")

    # 初始化
    path_config = __config__.get_path_config()
    camera_config = __config__.get_camera_config()
    qwen_config = __config__.get_api_config("qwen")
    qwen_vl_config = __config__.get_api_config("qwen_vl")
    deepseek_config = __config__.get_api_config("deepseek")
    robot_config = __config__.get_robot_config()
    assets_confog = __config__.get_assets_config()

    # 文件路径
    INPUT_IMAGE_PATH = path_config.get("input", {}).get("images")               # 输入照片路径
    OUTPUT_LOG_PATH = path_config.get("output", {}).get("logs")                 # 输出日志路径
    OUTPUT_UNIT_PATH = path_config.get("output", {}).get("units")               # 单元分割结果输出路径

    OCR_FILENAME = os.path.join(OUTPUT_LOG_PATH, "ocr_result.txt")              # OCR结果文件
    

    image_client = OpenCVImageClient(
        camera_config.get("id")
    )

    # robot_writer = RobotWritingClient(
    #     robot_config.get("com_port"),
    #     robot_config.get("baudrate"),
    #     robot_config.get("z_up"),
    #     robot_config.get("z_down"),
    #     robot_config.get("speed_move"),
    #     robot_config.get("speed_write"),
    #     robot_config.get("origin_x"),
    #     robot_config.get("origin_y"),
    #     assets_confog.get("chinese_fonts")
    # )

    qwen_client = QwenClient(
        api_key=qwen_config.get("api_key"),
        base_url=qwen_config.get("base_url"),
        vl_model=qwen_vl_config.get("model"),
        text_model=qwen_config.get("model")
    )

    pipeline_logger.info("=====================================================")
    pipeline_logger.info("===               Start the Pipeline              ===")
    pipeline_logger.info("=====================================================")
    pipeline_logger.info("")

    # robot_writer.write_chinese_char("你", 235.55, 0, 10)
    # robot_writer.write_ascii_char("D", 235.55, 0, 10)
    # robot_writer.write_text_line("牛的", 235.55, 0, 10, 10)
    # robot_writer.calibrate_origin()
    # robot_writer.stand_by()
    # robot_writer.write_text_line("你好, 高考试卷", 20, 10, 10, 1.1)
    # robot_writer.stand_by()

    # Step 1: 捕获图片
    pipeline_logger.info("=====================================================")
    pipeline_logger.info("===              Step1: Capture Image             ===")
    pipeline_logger.info("=====================================================")
    pipeline_logger.info("")

    image_list = image_client.capture_image(INPUT_IMAGE_PATH)




    # Step 2: OCR生成文本
    pipeline_logger.info("=====================================================")
    pipeline_logger.info("===                Step2: OCR Image               ===")
    pipeline_logger.info("=====================================================")
    pipeline_logger.info("")

    for index, image in enumerate(image_list):
        pipeline_logger.info(f"正在识别, 当前页码为{index}")
        qwen_client.ocr_image(image, OCR_FILENAME)




    # Step 3: 文本分割
    pipeline_logger.info("=====================================================")
    pipeline_logger.info("===                Step3: Text Split              ===")
    pipeline_logger.info("=====================================================")
    pipeline_logger.info("")

    full_text = read_txt_file(OCR_FILENAME)
    print(qwen_client.text_split(full_text))


    # Step 4: AI生成答案
    pipeline_logger.info("=====================================================")
    pipeline_logger.info("===            Step4: Answer Generation           ===")
    pipeline_logger.info("=====================================================")
    pipeline_logger.info("")

    # Step 5: 红框识别
    pipeline_logger.info("=====================================================")
    pipeline_logger.info("===             Step5: Box Recognition            ===")
    pipeline_logger.info("=====================================================")
    pipeline_logger.info("")

    # Step 6: 位置映射
    pipeline_logger.info("=====================================================")
    pipeline_logger.info("===             Step6: Position Mapping           ===")
    pipeline_logger.info("=====================================================")
    pipeline_logger.info("")

    # Step 7: 机械臂书写
    pipeline_logger.info("=====================================================")
    pipeline_logger.info("===              Step7: Robot Writing             ===")
    pipeline_logger.info("=====================================================")
    pipeline_logger.info("")

    pipeline_logger.info("=====================================================")
    pipeline_logger.info("===               Pipeline Finished               ===")
    pipeline_logger.info("=====================================================")

if __name__ == "__main__":
    main()