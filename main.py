import json
import uuid

from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import cast
from sqlalchemy.dialects.postgresql import JSON

from api.database import get_db, create_table
from api.cache import cache
from api.model import Pessoa
from .worker import insert_in_database
from api.schema import PessoaSchema


app = FastAPI()


@app.post("/pessoas")
async def store_pessoa(schema: PessoaSchema,):
    if cache.sismember("apelidos", schema.apelido):
        raise HTTPException(status_code=422, detail=f"O apelido {schema.apelido} já está em uso")
    
    cache.sadd("apelidos", schema.apelido)

    id_pessoa = str(uuid.uuid4())
    pessoa = Pessoa(id=id_pessoa, apelido=schema.apelido, nome=schema.nome, nascimento=schema.nascimento, stack=json.dumps(schema.stack))

    cache.set(id_pessoa, json.dumps(pessoa.dict()))
    insert_in_database.apply_async(args=[pessoa.dict()])

    return JSONResponse(content=id_pessoa, status_code=201, headers={"Location": f"/pessoas/{id_pessoa}"})


@app.get("/pessoas/{pessoa_id}")
async def get_pessoa(
    pessoa_id: str,
    database: AsyncSession = Depends(get_db)
):
    pessoa = cache.get(pessoa_id)
    if pessoa:
        pessoa = json.loads(pessoa)
        pessoa['stack'] = json.loads(pessoa['stack'])
        return pessoa
    
    pessoa = database.get(Pessoa, pessoa_id)
    if pessoa:
        pessoa.stack = json.loads(pessoa.stack)
        return pessoa

    raise HTTPException(status_code=404)


@app.get("/pessoas")
async def get_pessoas_by_term(
    t: str = Query(None, description="Termo da busca"),
    database: AsyncSession = Depends(get_db)
):
    if not t:
        raise HTTPException(status_code=400)
    query = select(
        Pessoa.id,
        Pessoa.apelido,
        Pessoa.nome,
        Pessoa.nascimento,
        cast(Pessoa.stack, JSON).label("stack")
    ).where(
        or_(
            Pessoa.nome.ilike(f"%{t}%"),
            Pessoa.apelido.ilike(f"%{t}%"),
            Pessoa.stack.ilike(f"%{t}%")
        )
    ).limit(50)
    result = await database.execute(query)
    return result.all()


@app.get("/contagem-pessoas")
async def count_pessoas(database: AsyncSession = Depends(get_db)):
    query = select(Pessoa)
    result = await database.execute(query)
    return len(result.all())


@app.on_event("startup")
async def startup_event():
    try:
        await create_table()
    except:
        pass
