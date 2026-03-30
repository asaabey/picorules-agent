#!/usr/bin/env node

import { compile, Dialect } from 'picorules-compiler-js-core';
import { readFileSync } from 'fs';
import { basename } from 'path';

const args = process.argv.slice(2);

if (args.length === 0) {
  console.error('Usage: node scripts/compile.mjs <file.prb> [dialect]');
  console.error('Dialects: mssql (default), oracle, postgresql');
  process.exit(1);
}

const filePath = args[0];
const dialectName = (args[1] || 'mssql').toLowerCase();

const dialectMap = {
  mssql: Dialect.MSSQL,
  oracle: Dialect.ORACLE,
  postgresql: Dialect.POSTGRESQL,
  postgres: Dialect.POSTGRESQL,
};

const dialect = dialectMap[dialectName];
if (!dialect) {
  console.error(`Unknown dialect: ${dialectName}. Use: mssql, oracle, postgresql`);
  process.exit(1);
}

const text = readFileSync(filePath, 'utf-8');
const name = basename(filePath, '.prb');

const result = compile(
  [{ name, text, isActive: true }],
  { dialect }
);

if (!result.success) {
  console.error('Compilation FAILED:');
  for (const err of result.errors) {
    console.error(`  [${err.ruleblock || '?'}${err.line ? ':' + err.line : ''}] ${err.message}`);
  }
  process.exit(1);
}

if (result.warnings.length > 0) {
  console.error('Warnings:');
  for (const w of result.warnings) {
    console.error(`  [${w.ruleblock || '?'}] ${w.message}`);
  }
}

if (result.metrics) {
  console.error(`Compiled in ${result.metrics.totalTimeMs}ms (parse: ${result.metrics.parseTimeMs}ms, sql: ${result.metrics.sqlGenTimeMs}ms)`);
}

for (const sql of result.sql) {
  console.log(sql);
  console.log('-- ---');
}
