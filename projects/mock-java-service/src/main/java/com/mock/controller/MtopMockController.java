package com.mock.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * MTOP Mock Controller - 修复数据结构
 */
@RestController
@RequestMapping("/mtop")
@CrossOrigin(origins = "*")
public class MtopMockController {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @RequestMapping(value = "/**", method = {RequestMethod.GET, RequestMethod.POST})
    public ResponseEntity<String> handleMtopRequest(
            @RequestParam(required = false) String api,
            HttpServletResponse response) throws IOException {
        
        response.setHeader("Access-Control-Allow-Origin", "*");
        response.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
        response.setContentType("application/json;charset=UTF-8");
        
        ObjectNode mockResponse = getMockData(api);
        String responseStr = objectMapper.writeValueAsString(mockResponse);
        
        return ResponseEntity.ok()
                .contentType(MediaType.APPLICATION_JSON)
                .body(responseStr);
    }

    private ObjectNode getMockData(String api) throws IOException {
        ObjectNode response = objectMapper.createObjectNode();
        response.putArray("ret").add("SUCCESS::调用成功");
        response.put("v", "1.0");
        response.put("traceId", "mock_" + System.currentTimeMillis());
        
        if (api == null) {
            response.set("data", objectMapper.createObjectNode());
            return response;
        }
        
        switch (api) {
            case "mtop.alibaba.jp.guide.page.get":
                response.set("data", getGuidePageData());
                break;
            case "mtop.relationrecommend.tiantaojprecommend.recommend":
            case "mtop.relationrecommend.TianTaoJpRecommend.recommend":
                response.set("data", getRecommendData());
                break;
            default:
                response.set("data", objectMapper.createObjectNode());
        }
        
        return response;
    }

    private ObjectNode getGuidePageData() throws IOException {
        ObjectNode data = objectMapper.createObjectNode();
        data.put("pageCode", "541699");
        data.put("pageName", "新分类 - 女性穿搭");
        
        ArrayNode cardGroups = objectMapper.createArrayNode();
        
        // Card 1: xiaowupinlei1
        ObjectNode card1 = createCard(
            "xiaowupinlei1",
            "小物品类 1",
            createItems(new String[][]{
                {"1001006104017075", "レディース ボストン型 ショルダーバッグ", "9267", "10267", "9", "S1e5850ba5b9a49f89a8616f1ef8cb26ad", "0"},
                {"1001006096311386", "大容量 本革トートバッグ", "8362", "9362", "10", "S1e24bf6eabbf4e56a2c6ff136fd290fbf", "76"},
                {"1001006098713583", "レトロデザインの大容量本革トートバッグ", "7852", "8852", "11", "S98154f84cc8f45c1831f2a07d2c1c968U", "1"},
                {"1001006107296768", "極上の柔らかさの腋下バッグ", "26225", "27225", "3", "S1e5850ba5b9a49f89a8616f1ef8cb26ad", "123"}
            })
        );
        cardGroups.add(card1);
        
        // Card 2: xiaowupinlei3
        ObjectNode card2 = createCard(
            "xiaowupinlei3",
            "旅をラクにするスーツケース厳選",
            createItems(new String[][]{
                {"1001006107613343", "男女兼用 本革 羊革製 トラベルバッグ", "4208", "5208", "19", "Sfbc4c5b070274debb049f792bd085aa9Y", "10"},
                {"1001006097916009", "大容量アルミフレーム旅行カバン", "7872", "8872", "11", "Sfb7d7599c9cc456f99e99b0895f6fc7cU", "3"},
                {"1001006107198446", "ヴィンテージクレイジーホーススキントラベルバッグ", "10971", "11971", "8", "S3810ca1b1e7943dcae43550705e4b7bbD", "14"},
                {"1001006098003196", "軽量で堅牢なキャリーケース", "5425", "6425", "15", "Sa425b95ac3054077b67473c3dfe929b1Y", "181"}
            })
        );
        cardGroups.add(card2);
        
        data.set("cardGroups", cardGroups);
        return data;
    }

    private ObjectNode createCard(String cardCode, String title, ArrayNode items) {
        ObjectNode card = objectMapper.createObjectNode();
        card.put("cardCode", cardCode);
        card.put("identityName", "channelPageStandardCard");
        
        // 前端期望：item?.elements?.[0]?.contentInfo?.itemList
        // 所以 elements 应该在 card 的顶层，不是在 contentInfo 里面
        
        // contentInfo 只包含 productCardInfo 和 moduleConfig
        ObjectNode contentInfo = objectMapper.createObjectNode();
        
        ObjectNode productCardInfo = objectMapper.createObjectNode();
        productCardInfo.put("showDiscountTag", true);
        productCardInfo.put("cardRows", "1");
        productCardInfo.put("cardContainerSize", "3:4");
        contentInfo.set("productCardInfo", productCardInfo);
        
        ObjectNode moduleConfig = objectMapper.createObjectNode();
        moduleConfig.put("customSpmc", cardCode);
        moduleConfig.put("title", title);
        contentInfo.set("moduleConfig", moduleConfig);
        
        card.set("contentInfo", contentInfo);
        
        // elements 数组在 card 的顶层
        ArrayNode elementsArray = objectMapper.createArrayNode();
        
        // 每个 element 包含 contentInfo
        ObjectNode element = objectMapper.createObjectNode();
        ObjectNode elementContentInfo = objectMapper.createObjectNode();
        elementContentInfo.set("itemList", items);
        elementContentInfo.put("isDiscountExist", true);
        element.set("contentInfo", elementContentInfo);
        
        elementsArray.add(element);
        card.set("elements", elementsArray);
        
        return card;
    }

    private ArrayNode createItems(String[][] items) {
        ArrayNode itemList = objectMapper.createArrayNode();
        
        for (String[] item : items) {
            ObjectNode itemObj = objectMapper.createObjectNode();
            
            // 必需字段
            itemObj.put("productId", item[0]);
            itemObj.put("itemId", Long.parseLong(item[0]));
            itemObj.put("title", item[1]);
            itemObj.put("imgUrl", "https://pic-cdn-jp.tao-media.co/kf/" + item[5] + ".jpg_400x400q75.jpg_.webp");
            itemObj.put("itemImage", "https://pic-cdn-jp.tao-media.co/kf/" + item[5] + ".jpg_400x400q75.jpg_.webp");
            
            // prices.formattedPrice
            ObjectNode prices = objectMapper.createObjectNode();
            prices.put("formattedPrice", "¥ " + formatPrice(item[2]));
            itemObj.set("prices", prices);
            
            // itemPrice
            ObjectNode price = objectMapper.createObjectNode();
            price.put("cent", Integer.parseInt(item[2]));
            price.put("currencySymbol", "¥");
            price.put("discountRate", Integer.parseInt(item[4]));
            price.put("originalPrice", "¥ " + formatPrice(item[3]));
            price.put("priceInfo", "¥ " + formatPrice(item[2]));
            price.put("priceString", item[2]);
            price.put("color", "#333333");
            price.put("discountRateLineBreak", item[4] + "%-OFF");
            price.put("displayText", item[4] + "%OFF");
            price.put("originalCent", Integer.parseInt(item[3]));
            itemObj.set("itemPrice", price);
            
            // itemStatus
            ObjectNode status = objectMapper.createObjectNode();
            status.put("status", 1);
            status.put("displayText", "購入できない商品");
            status.put("statusText", "下架");
            itemObj.set("itemStatus", status);
            
            itemObj.put("sales", Integer.parseInt(item[6]));
            
            itemList.add(itemObj);
        }
        
        return itemList;
    }

    private ObjectNode getRecommendData() {
        ObjectNode data = objectMapper.createObjectNode();
        ArrayNode result = objectMapper.createArrayNode();
        
        ObjectNode resultItem = objectMapper.createObjectNode();
        ObjectNode mods = objectMapper.createObjectNode();
        mods.set("listItems", createRecommendItems());
        resultItem.set("mods", mods);
        
        ArrayNode layoutInfo = objectMapper.createArrayNode();
        layoutInfo.add("rcmdTitle");
        resultItem.set("layoutInfo", layoutInfo);
        
        result.add(resultItem);
        
        ObjectNode rcmdTitle = objectMapper.createObjectNode();
        rcmdTitle.put("title", "RECOMMEND");
        rcmdTitle.put("tItemType", "nt_rcmd_title");
        
        data.set("result", result);
        data.set("rcmdTitle", rcmdTitle);
        
        return data;
    }

    private ArrayNode createRecommendItems() {
        ArrayNode itemList = objectMapper.createArrayNode();
        
        for (String[] item : new String[][]{
            {"1001006107296768", "極上の柔らかさの腋下バッグ", "26225", "27225", "3", "S1e5850ba5b9a49f89a8616f1ef8cb26ad", "123"},
            {"1001006096311386", "大容量 本革トートバッグ", "8362", "9362", "10", "S1e24bf6eabbf4e56a2c6ff136fd290fbf", "76"}
        }) {
            ObjectNode itemObj = objectMapper.createObjectNode();
            
            itemObj.put("productId", item[0]);
            itemObj.put("itemId", Long.parseLong(item[0]));
            
            // title 应该是对象，包含 displayTitle（推荐组件需要）
            ObjectNode titleObj = objectMapper.createObjectNode();
            titleObj.put("displayTitle", item[1]);
            titleObj.put("rowNum", 1);
            itemObj.set("title", titleObj);
            
            itemObj.put("imgUrl", "https://pic-cdn-jp.tao-media.co/kf/" + item[5] + ".jpg_400x400q75.jpg_.webp");
            itemObj.put("itemImage", "https://pic-cdn-jp.tao-media.co/kf/" + item[5] + ".jpg_400x400q75.jpg_.webp");
            
            // image 对象（推荐组件需要）
            ObjectNode image = objectMapper.createObjectNode();
            image.put("imgUrl", "https://pic-cdn-jp.tao-media.co/kf/" + item[5] + ".jpg_400x400q75.jpg_.webp");
            image.put("imgType", "3:4");
            itemObj.set("image", image);
            
            // prices
            ObjectNode prices = objectMapper.createObjectNode();
            prices.put("formattedPrice", "¥ " + formatPrice(item[2]));
            prices.put("salePrice", "¥ " + formatPrice(item[2]));
            prices.put("originalPrice", "¥ " + formatPrice(item[3]));
            itemObj.set("prices", prices);
            
            // itemPrice
            ObjectNode price = objectMapper.createObjectNode();
            price.put("cent", Integer.parseInt(item[2]));
            price.put("currencySymbol", "¥");
            price.put("discountRate", Integer.parseInt(item[4]));
            price.put("originalPrice", "¥ " + formatPrice(item[3]));
            price.put("priceInfo", "¥ " + formatPrice(item[2]));
            price.put("priceString", item[2]);
            price.put("color", "#333333");
            price.put("discountRateLineBreak", item[4] + "%-OFF");
            price.put("displayText", item[4] + "%OFF");
            price.put("originalCent", Integer.parseInt(item[3]));
            itemObj.set("itemPrice", price);
            
            // itemStatus
            ObjectNode status = objectMapper.createObjectNode();
            status.put("status", 1);
            status.put("displayText", "購入できない商品");
            status.put("statusText", "下架");
            itemObj.set("itemStatus", status);
            
            itemObj.put("sales", Integer.parseInt(item[6]));
            
            // sellingPoints（推荐组件需要）
            ArrayNode sellingPoints = objectMapper.createArrayNode();
            ObjectNode point = objectMapper.createObjectNode();
            point.put("displayText", "好評アイテム");
            point.put("pointType", "POSITIVE_EVALUATION_POINT");
            sellingPoints.add(point);
            itemObj.set("sellingPoints", sellingPoints);
            
            // trace
            ObjectNode trace = objectMapper.createObjectNode();
            trace.put("utLogMap", "{}");
            itemObj.set("trace", trace);
            
            itemList.add(itemObj);
        }
        
        return itemList;
    }

    private String formatPrice(String priceStr) {
        return String.format("%,d", Integer.parseInt(priceStr));
    }
}
