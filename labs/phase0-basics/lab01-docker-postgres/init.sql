-- 初始化表结构：模拟一个简单的电商订单表
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    product VARCHAR(200) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    order_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'pending'
);

-- 插入 10 条测试数据
INSERT INTO orders (customer_name, product, amount, order_date, status) VALUES
('张三', '机械键盘', 399.00, '2026-06-01', 'completed'),
('李四', '显示器 27寸', 1899.00, '2026-06-02', 'completed'),
('王五', '蓝牙耳机', 259.00, '2026-06-03', 'shipped'),
('张三', '鼠标垫', 49.00, '2026-06-04', 'completed'),
('赵六', 'Type-C 数据线', 29.90, '2026-06-05', 'pending'),
('李四', 'USB 扩展坞', 329.00, '2026-06-06', 'completed'),
('孙七', '机械键盘', 459.00, '2026-06-08', 'shipped'),
('王五', '摄像头 1080p', 199.00, '2026-06-09', 'pending'),
('张三', '显示器支架', 159.00, '2026-06-10', 'completed'),
('赵六', '无线鼠标', 129.00, '2026-06-12', 'shipped');

-- 开启 pgvector 扩展
CREATE EXTENSION IF NOT EXISTS vector;

-- 创建一个带向量的表（为后续 AI 实验做准备）
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536)  -- OpenAI text-embedding-3-small 的维度
);
