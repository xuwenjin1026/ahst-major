# 安徽科技工程大学高考专业推荐系统

面向安徽考生的智能专业推荐工具，根据高考分数、选科类型智能匹配可报考专业，按冲/稳/保分层推荐。

## 项目结构

```
ahst-major-recommendation/
├── backend/                 # Django后端
│   ├── ahst_project/        # Django项目配置
│   ├── api/                 # 主要应用
│   ├── manage.py            # Django管理脚本
│   └── requirements.txt     # Python依赖
├── frontend/                # Vue3前端
│   ├── src/
│   │   ├── components/      # Vue组件
│   │   ├── views/           # 页面视图
│   │   ├── router/          # 路由配置
│   │   ├── utils/           # 工具函数
│   │   ├── App.vue          # 根组件
│   │   └── main.js          # 入口文件
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── database/                # 数据库相关
│   ├── schema.sql           # 数据库表结构
│   └── import_data.py       # 数据导入脚本
└── README.md                # 项目文档
```

## 技术栈

### 后端
- Django 4.2
- Django REST Framework 3.14
- MySQL 8.0+
- Python 3.9+

### 前端
- Vue 3.3
- Vite 4.5
- Element Plus 2.4
- ECharts 5.4
- Axios

## 功能特性

1. **智能推荐算法**
   - 分数转位次转换
   - 冲稳保三层梯度推荐
   - 多维度匹配分析

2. **丰富数据展示**
   - 历年分数线可视化趋势图
   - 专业详情弹窗
   - 就业前景分析
   - 王牌专业高亮标识

3. **灵活筛选功能**
   - 校区筛选（蚌埠、滁州、凤阳）
   - 选科类型切换（物理/历史）
   - 专业分类筛选

4. **移动端适配**
   - 响应式设计
   - 手机端友好界面
   - 轻量化部署

## 快速开始

### 环境准备

1. **安装Python 3.9+**
   ```bash
   python --version
   ```

2. **安装Node.js 16+**
   ```bash
   node --version
   npm --version
   ```

3. **安装MySQL 8.0+**
   ```bash
   mysql --version
   ```

### 后端部署

1. **创建数据库**
   ```bash
   mysql -u root -p
   source database/schema.sql
   ```

2. **配置环境变量**
   ```bash
   cd backend
   cp .env.example .env
   # 编辑.env文件，配置数据库连接信息
   ```

3. **安装Python依赖**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **数据库迁移**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **导入示例数据**
   ```bash
   cd database
   python import_data.py
   ```

6. **启动开发服务器**
   ```bash
   cd backend
   python manage.py runserver 0.0.0.0:8000
   ```

### 前端部署

1. **安装依赖**
   ```bash
   cd frontend
   npm install
   ```

2. **启动开发服务器**
   ```bash
   npm run dev
   ```

3. **访问应用**
   打开浏览器访问：http://localhost:3000

### 生产环境部署

#### 后端

1. **修改配置**
   编辑 `backend/ahst_project/settings.py`：
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['your-domain.com']
   ```

2. **收集静态文件**
   ```bash
   python manage.py collectstatic
   ```

3. **使用Nginx + uWSGI部署**
   ```bash
   pip install uwsgi
   uwsgi --ini uwsgi.ini
   ```

#### 前端

1. **构建生产版本**
   ```bash
   cd frontend
   npm run build
   ```

2. **部署静态文件**
   将 `frontend/dist` 目录内容部署到Nginx

## API接口文档

### 1. 获取校区列表
- **URL**: `/api/campuses/`
- **方法**: GET
- **返回**: 校区列表

### 2. 获取专业分类
- **URL**: `/api/categories/`
- **方法**: GET
- **返回**: 专业分类列表

### 3. 专业推荐
- **URL**: `/api/recommend/`
- **方法**: POST
- **参数**:
  ```json
  {
    "score": 450,
    "subject_type": "physics",
    "campus_filter": ["蚌埠校区"],
    "category_filter": []
  }
  ```
- **返回**: 冲稳保三层推荐结果

### 4. 获取专业详情
- **URL**: `/api/majors/{major_id}/`
- **方法**: GET
- **参数**: `subject_type`
- **返回**: 专业详细信息

### 5. 分数转位次
- **URL**: `/api/rank/query/`
- **方法**: GET
- **参数**: `score`, `subject_type`, `year`
- **返回**: 位次信息

### 6. 分数线趋势
- **URL**: `/api/majors/{major_id}/trend/`
- **方法**: GET
- **参数**: `subject_type`, `years`
- **返回**: 历年分数线趋势数据

## 核心算法说明

### 冲稳保阈值配置

```python
{
  'chong': {
    'rank_ratio_min': 0.85,  # 位次比例下限
    'rank_ratio_max': 1.0,   # 位次比例上限
    'score_diff_min': -5,    # 分数差下限
    'score_diff_max': 0      # 分数差上限
  },
  'wen': {
    'rank_ratio_min': 1.0,
    'rank_ratio_max': 1.2,
    'score_diff_min': -15,
    'score_diff_max': -5
  },
  'bao': {
    'rank_ratio_min': 1.2,
    'rank_ratio_max': 1.5,
    'score_diff_min': -30,
    'score_diff_max': -15
  }
}
```

**判断逻辑**：
- 位次比例 = 用户位次 / 专业最低位次
- 比例 > 1 表示用户位次更低（排名更靠后），录取可能性更大
- 分数差 = 用户分数 - 专业最低分
- 正值表示用户分数高于专业最低分

## 数据导入

### 手动导入真实数据

1. **准备Excel数据文件**
   - 专业信息表
   - 历年分数线表
   - 位次对照表

2. **修改导入脚本**
   编辑 `database/import_data.py`，替换示例数据为真实数据

3. **执行导入**
   ```bash
   python database/import_data.py
   ```

## 常见问题

### 1. 数据库连接失败
检查 `.env` 文件中的数据库配置是否正确：
```bash
DB_NAME=ahst_major_recommendation
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

### 2. 前端无法连接后端API
检查 Vite 代理配置 `frontend/vite.config.js`：
```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true
  }
}
```

### 3. ECharts图表不显示
确保组件中正确引入了ECharts：
```javascript
import * as echarts from 'echarts'
```

## 更新日志

### v1.0.0 (2024-01-01)
- 完整的前后端功能
- 冲稳保推荐算法
- 数据可视化
- 移动端适配

## 许可证

本项目仅供学习和参考使用。

## 联系方式

如有问题或建议，请提交Issue。