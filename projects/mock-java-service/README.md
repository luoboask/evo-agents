# MTOP Mock Java Service

基于 Spring Boot 的 MTOP API Mock 服务

## 功能

- ✅ 提供 `mtop.alibaba.jp.guide.page.get` 接口
- ✅ 提供 `mtop.relationrecommend.TianTaoJpRecommend.recommend` 接口
- ✅ 提供 `mtop.jptao.ug.popx.check` 接口
- ✅ 提供 `mtop.jptao.ug.popx.list` 接口
- ✅ 提供 `mtop.jp.wishlist.item.add` 接口
- ✅ 提供 `mtop.jp.interaction.execute` 接口
- ✅ 支持 CORS 跨域
- ✅ 返回真实商品数据

## 快速启动

### 方式 1: 使用启动脚本

```bash
chmod +x start.sh
./start.sh
```

### 方式 2: 使用 Maven

```bash
cd /Users/dhr/.openclaw/workspace/projects/mock-java-service
mvn clean package -DskipTests
java -jar target/mock-java-service-1.0.0.jar
```

## 访问地址

- **服务地址**: http://localhost:8090
- **健康检查**: http://localhost:8090/actuator/health

## API 示例

### 1. 导购页面

```bash
curl "http://localhost:8090/mtop/comet/async.api?api=mtop.alibaba.jp.guide.page.get&v=1.0&data={}"
```

### 2. 推荐商品

```bash
curl "http://localhost:8090/mtop/comet/async.api?api=mtop.relationrecommend.TianTaoJpRecommend.recommend&v=1.0"
```

### 3. 弹窗检查

```bash
curl "http://localhost:8090/mtop/comet/async.api?api=mtop.jptao.ug.popx.check&v=1.0"
```

## 前端配置

修改前端的 MTOP 拦截器，直接请求 Java 服务：

```javascript
const MOCK_SERVER_URL = 'http://localhost:8090/mtop/comet/async.api';

mtop.request = function(api, params, callback) {
  const url = MOCK_SERVER_URL + '?api=' + api + '&v=1.0';
  
  fetch(url)
    .then(res => res.json())
    .then(data => {
      if (typeof callback === 'function') callback(null, data);
    })
    .catch(err => {
      if (typeof callback === 'function') callback(err);
    });
};
```

## 数据结构

所有 Mock 数据都来自 `mockData.txt`，包含真实的商品信息：

- itemId: 商品 ID
- itemImage: 商品图片
- itemPrice: 商品价格（包含 cent, currencySymbol, discountRate, priceInfo 等）
- itemStatus: 商品状态
- sales: 销量
- supplementSellingPoints: 卖点标签

## 技术栈

- Spring Boot 2.7.0
- FastJSON 2.0.0
- Maven
- Java 11
