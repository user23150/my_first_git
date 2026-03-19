##sk-ea8c57725bf64570a9418e2807e31913

from langchain_community.llm import Tongyi

# 加载环境变量（也可直接赋值API_KEY）
load_dotenv()
os.environ["ZHIPUAI_API_KEY"] = "sk-ea8c57725bf64570a9418e2807e31913"  # 替换为自己的API_KEY

# 1. 定义智能体的工具（示例：两个简单工具）
def get_weather(city: str) -> str:
    """获取指定城市的天气（模拟接口，免费无调用成本）"""
    # 实际场景可替换为免费天气API，如高德/百度天气免费接口
    weather_data = {
        "北京": "晴，10-20℃",
        "上海": "多云，12-18℃",
        "广州": "阴，18-25℃"
    }
    return f"{city}的天气：{weather_data.get(city, '暂未查询到该城市天气')}"

def calculate_math(expression: str) -> str:
    """计算简单数学表达式（如1+2*3）"""
    try:
        result = eval(expression)  # 仅示例，生产环境需替换为安全的计算方式
        return f"计算结果：{expression} = {result}"
    except:
        return "计算失败，请输入合法的数学表达式（如1+2*3）"

# 封装工具（LangChain标准格式）
tools = [
    Tool(
        name="get_weather",
        func=get_weather,
        description="用于查询城市的天气信息，输入参数为城市名称（如北京、上海）"
    ),
    Tool(
        name="calculate_math",
        func=calculate_math,
        description="用于计算简单数学表达式，输入参数为数学表达式（如1+2*3）"
    )
]

# 2. 初始化免费的LLM（智谱AI GLM-4免费版）
llm = ChatZhipuAI(
    model="glm-4-free",  # 免费版模型
    temperature=0.1,     # 随机性，0为最稳定
    api_key=os.environ["ZHIPUAI_API_KEY"]
)

# 3. 定义智能体的提示词（指导智能体如何使用工具）
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个乐于助人的智能体，会根据用户需求选择合适的工具解决问题。"),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}")  # 智能体思考过程的占位符
])

# 4. 创建并运行智能体
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 测试智能体
if __name__ == "__main__":
    # 测试1：查询天气
    print("===== 测试1：查询天气 =====")
    result1 = agent_executor.invoke({"input": "北京今天的天气怎么样？"})
    print(result1["output"])

    # 测试2：计算数学题
    print("\n===== 测试2：计算数学题 =====")
    result2 = agent_executor.invoke({"input": "帮我算一下100-23*3等于多少？"})
    print(result2["output"])

    # 测试3：无需工具的问答
    print("\n===== 测试3：普通问答 =====")
    result3 = agent_executor.invoke({"input": "解释一下什么是LangChain智能体？"})
    print(result3["output"])