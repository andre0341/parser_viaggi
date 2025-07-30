import express from 'express';
import sqlite3 from 'sqlite3';
import path from 'path';
import { fileURLToPath } from 'url';

const app = express();
const db = new sqlite3.Database('db.sqlite');

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.use(express.static(path.join(__dirname, 'public')));

function buildWhere(query) {
  const clauses = [];
  const params = [];
  if (query.country) {
    clauses.push('country = ?');
    params.push(query.country);
  }
  if (query.formula) {
    clauses.push('formula = ?');
    params.push(query.formula);
  }
  if (query.airport) {
    clauses.push('airport = ?');
    params.push(query.airport);
  }
  const where = clauses.length ? `WHERE ${clauses.join(' AND ')}` : '';
  return { where, params };
}

app.get('/api/offers', (req, res) => {
  const { where, params } = buildWhere(req.query);
  const sort = ['price', 'date', 'country'].includes(req.query.sortBy)
    ? `ORDER BY ${req.query.sortBy}`
    : '';
  db.all(
    `SELECT * FROM offers ${where} ${sort}`,
    params,
    (err, rows) => {
      if (err) return res.status(500).json({ error: err.message });
      res.json(rows);
    }
  );
});

app.get('/api/filters', (req, res) => {
  const result = {};
  const fields = ['country', 'formula', 'airport'];
  let pending = fields.length;
  fields.forEach((f) => {
    db.all(`SELECT DISTINCT ${f} FROM offers`, [], (err, rows) => {
      if (!err) result[f] = rows.map((r) => r[f]);
      if (--pending === 0) res.json(result);
    });
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Dashboard listening on ${PORT}`));
