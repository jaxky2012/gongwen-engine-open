/**
 * 宣传图片导出脚本
 * 使用方法: node export-images.js
 * 需要先安装: npm install puppeteer
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const OUTPUT_DIR = path.join(__dirname, 'images');
const HTML_FILE = path.join(__dirname, 'promo-images.html');

// 确保输出目录存在
if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// 图片导出配置
const images = [
    { name: '01-banner', selector: '.promo-card:nth-child(1)', width: 1400, height: 450 },
    { name: '02-compare', selector: '.promo-card:nth-child(2)', width: 1200, height: 550 },
    { name: '03-flow', selector: '.promo-card:nth-child(3)', width: 1200, height: 480 },
    { name: '04-sample', selector: '.promo-card:nth-child(4)', width: 1200, height: 750 }
];

async function exportImages() {
    console.log('启动浏览器...');
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    try {
        const page = await browser.newPage();

        console.log('加载HTML文件...');
        await page.goto(`file://${HTML_FILE}`, {
            waitUntil: 'networkidle0'
        });

        console.log('\n开始导出图片...\n');

        for (const img of images) {
            console.log(`导出: ${img.name}.png`);

            // 等待元素加载
            await page.waitForSelector(img.selector);

            // 获取元素
            const element = await page.$(img.selector);

            if (element) {
                // 设置视口大小
                await page.setViewport({
                    width: img.width + 100,
                    height: img.height + 100,
                    deviceScaleFactor: 2 // 2x分辨率
                });

                // 截图
                await element.screenshot({
                    path: path.join(OUTPUT_DIR, `${img.name}.png`),
                    type: 'png'
                });

                console.log(`  完成: ${img.name}.png (${img.width}x${img.height})`);
            } else {
                console.log(`  跳过: 未找到元素 ${img.selector}`);
            }
        }

        console.log('\n全部导出完成!');
        console.log(`输出目录: ${OUTPUT_DIR}`);

    } catch (error) {
        console.error('导出失败:', error.message);
    } finally {
        await browser.close();
    }
}

// 运行导出
exportImages();
