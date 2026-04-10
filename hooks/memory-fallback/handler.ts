#!/usr/bin/env node
/**
 * Memory Fallback Hook Handler
 * 
 * 在 OpenClaw 原始记忆未找到时，自动从 memory-search 查询
 */

import { spawn } from 'child_process';
import { join } from 'path';

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || '/Users/dhr/.openclaw/workspace-claude-code-agent';
const MEMORY_SEARCH_SCRIPT = join(WORKSPACE, 'skills/memory-search/unified_search.py');

interface HookContext {
    user_message: string;
    system_prompt: string;
    agent_name: string;
    [key: string]: any;
}

interface SearchResult {
    source: string;
    content: string;
    score: number;
}

/**
 * 检测是否需要查询记忆
 */
function shouldSearch(message: string): boolean {
    const triggerKeywords = [
        '之前', '以前', '历史', '记得', '说过', '问过',
        '配置', '怎么', '如何', '什么', '哪里',
        '项目', '系统', '任务', '部署', '安装'
    ];
    
    const messageLower = message.toLowerCase();
    return triggerKeywords.some(keyword => messageLower.includes(keyword.toLowerCase()));
}

/**
 * 调用 memory-search 查询
 */
async function searchMemory(query: string, topK: number = 5): Promise<SearchResult[]> {
    return new Promise((resolve, reject) => {
        const args = [
            MEMORY_SEARCH_SCRIPT,
            query,
            '--top-k', topK.toString(),
            '--agent', process.env.OPENCLAW_AGENT_NAME || 'claude-code-agent'
        ];
        
        const python = spawn('python3', args, {
            cwd: WORKSPACE,
            env: { ...process.env, PYTHONPATH: WORKSPACE }
        });
        
        let output = '';
        let error = '';
        
        python.stdout.on('data', (data) => {
            output += data.toString();
        });
        
        python.stderr.on('data', (data) => {
            error += data.toString();
        });
        
        python.on('close', (code) => {
            if (code === 0) {
                // 解析输出
                const results: SearchResult[] = [];
                const lines = output.split('\n');
                
                for (const line of lines) {
                    const match = line.match(/\d+\.\s+\[([^\]]+)\]\s+(.+)/);
                    if (match) {
                        results.push({
                            source: match[1],
                            content: match[2],
                            score: 1.0
                        });
                    }
                }
                
                resolve(results);
            } else {
                reject(new Error(`Python script failed: ${error}`));
            }
        });
    });
}

/**
 * 构建上下文
 */
function buildContext(results: SearchResult[]): string {
    if (results.length === 0) {
        return '';
    }
    
    const parts = results.map(r => `[${r.source}] ${r.content.substring(0, 300)}`);
    return `\n\n相关记忆:\n${parts.join('\n\n')}`;
}

/**
 * Hook 主函数 - 在 LLM 调用前执行
 */
export async function beforeLLMCall(context: HookContext): Promise<HookContext> {
    const { user_message, system_prompt } = context;
    
    // 检查是否需要查询
    if (!shouldSearch(user_message)) {
        return context;
    }
    
    try {
        // 查询记忆
        const results = await searchMemory(user_message, 5);
        
        if (results.length === 0) {
            return context;
        }
        
        // 构建上下文
        const memoryContext = buildContext(results);
        
        // 增强系统提示
        context.system_prompt = system_prompt + memoryContext;
        
        console.log(`[memory-fallback] Enhanced context with ${results.length} memories`);
        
    } catch (error) {
        console.error('[memory-fallback] Error:', error);
    }
    
    return context;
}

/**
 * Hook 元数据
 */
export const hook = {
    name: 'memory-fallback',
    description: 'Automatically query memory-search when OpenClaw memory not found',
    version: '1.0.0',
    events: ['before_llm_call'],
    requirements: {
        python: '>=3.9',
        workspace: true
    }
};
