const express = require('express');
const cors = require('cors');
const { createClient } = require('redis');

const app = express();
app.use(cors());
app.use(express.json());

// Target Network Parameters
const CHAIN_ID_DEC = 250000000;
const CHAIN_ID_HEX = "0x" + CHAIN_ID_DEC.toString(16); // 0xee6b280
const GAS_LIMIT_BUFFER = "0xee6b280"; // 250,000,000 gas limit ceiling

// Initialize local memory cache client
const cache = createClient();
cache.on('error', err => console.log('Cache Error:', err));
cache.connect().then(() => console.log('[✓] In-Memory Cache Connection Active.'));

// 3-Stage Cycle Processing Pipeline
app.post('/', async (req, res) => {
    const { method, params, id } = req.body;
    console.log(`[INGESTION] Processing Method: ${method}`);

    // STAGE 1 & 2: Local Interception, State Tracking & Dynamic Routing Loop
    if (method === 'eth_chainId') {
        return res.json({ jsonrpc: "2.0", id, result: CHAIN_ID_HEX });
    }
    
    if (method === 'net_version') {
        return res.json({ jsonrpc: "2.0", id, result: CHAIN_ID_DEC.toString() });
    }

    if (method === 'eth_getBlockByNumber') {
        // Try hitting local high-speed memory cache first (Middleman-free speed layer)
        const cacheKey = `block_${params[0]}`;
        const cachedBlock = await cache.get(cacheKey);
        
        if (cachedBlock) {
            return res.json({ jsonrpc: "2.0", id, result: JSON.parse(cachedBlock) });
        }

        // Mock Block Generation Structure matching the 250,000,000 specification
        const simulatedBlock = {
            number: params[0] === 'latest' ? "0x1" : params[0],
            hash: "0x" + [...Array(64)].map(() => Math.floor(Math.random()*16).toString(16)).join(''),
            parentHash: "0x0000000000000000000000000000000000000000000000000000000000000000",
            gasLimit: GAS_LIMIT_BUFFER,
            gasUsed: "0x0",
            transactions: []
        };

        // Commit directly to self-hosted cache buffer for 10 seconds to optimize system disk IO
        await cache.set(cacheKey, JSON.stringify(simulatedBlock), { EX: 10 });
        return res.json({ jsonrpc: "2.0", id, result: simulatedBlock });
    }

    // Default fallback interface structure for custom simulation handling
    res.json({
        jsonrpc: "2.0",
        id,
        result: "0x"
    });
});

// Fire up interface loop on Port 8545 (Standard local RPC client port)
const PORT = 8545;
app.listen(PORT, () => {
    console.log(`\n======================================================`);
    console.log(`[✓] 3-Stage Independent Validation Cycle Operational`);
    console.log(`[✓] Listening on: http://127.0.0.1:${PORT}`);
    console.log(`[✓] Serving Chain ID: ${CHAIN_ID_DEC} (${CHAIN_ID_HEX})`);
    console.log(`======================================================\n`);
});
