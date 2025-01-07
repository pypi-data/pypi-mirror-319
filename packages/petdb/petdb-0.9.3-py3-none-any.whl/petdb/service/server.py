
import os
import time
import hashlib
import threading
import asyncio
from queue import Queue
from typing import Callable, Any

import uvicorn
from fastapi import FastAPI, Request, Response, status, Body

from petdb import PetDB, PetCollection, PetArray

STORAGE_PATH = "/var/lib/petdb"

app = FastAPI()

@app.post("/collections")
def get_collections(request: Request):
	return request.state.db.collections()

@app.post("/drop")
def drop_collections(request: Request):
	request.state.db.drop()

@app.post("/drop/{name}")
def drop_collection(request: Request, name: str):
	request.state.db.drop_collection(name)

@app.post("/mutate/{name}")
def mutate(request: Request, name: str, mutations: list[dict] = Body(embed=True)):
	array = request.state.db.collection(name)
	for mutation in mutations:
		array: PetArray = array.__getattribute__(mutation["type"])(*mutation["args"])
	return array.list()

@app.post("/insert/{name}")
def insert(request: Request, name: str, doc: dict = Body(embed=True)):
	return request.state.db.collection(name).insert(doc)

@app.post("/insert_many/{name}")
def insert_many(request: Request, name: str, docs: list[dict] = Body(embed=True)):
	return request.state.db.collection(name).insert_many(docs)

@app.post("/update_one/{name}")
def update_one(request: Request, name: str, update: dict = Body(embed=True), query: dict = Body(embed=True)):
	return request.state.db.collection(name).update_one(update, query)

@app.post("/update/{name}")
def update(request: Request, name: str, update: dict = Body(embed=True), query: dict = Body(embed=True)):
	return request.state.db.collection(name).update(update, query)

@app.post("/remove/{name}")
def remove(request: Request, name: str, query: dict = Body(embed=True)):
	return request.state.db.collection(name).remove(query)

@app.post("/clear/{name}")
def clear(request: Request, name: str):
	return request.state.db.collection(name).clear()


class Cache[T]:

	def __init__(self, factory: Callable[..., T]):
		self.factory = factory
		self.instances = {}

	def get(self, key, *args) -> T:
		if key not in self.instances:
			self.instances[key] = self.factory(key, *args)
		return self.instances[key]

class Server:

	LOCK_TIMEOUT = 5 * 60 # 5 min

	def __init__(self, port: int, passwords: dict[str, str]):
		self.passwords = passwords
		self.port = port
		self.db = Cache(self.create_db_object)
		self.tasks = Cache(lambda name: Queue())

	def create_db_object(self, name: str) -> PetDB:
		threading.Thread(target=self.process_requests, args=(name,), daemon=True).start()
		return PetDB.get(os.path.join(STORAGE_PATH, name))

	def run(self):

		@app.middleware("http")
		async def middleware(request: Request, call_next):
			body = await request.json()
			dbname = body.get("dbname")
			password = body.get("password")
			if dbname is None or dbname not in self.passwords:
				return Response(status_code=status.HTTP_400_BAD_REQUEST)
			if password is None or hashlib.sha256(password.encode("utf-8")).hexdigest() != self.passwords[dbname]:
				return Response(status_code=status.HTTP_401_UNAUTHORIZED)
			request.state.db = self.db.get(dbname)
			result = Queue(maxsize=1)
			self.tasks.get(dbname).put((call_next, (request,), result))
			value = await asyncio.to_thread(result.get)
			if isinstance(value, Response):
				return value
			else:
				return Response(content=str(value), status_code=500)

		# noinspection PyDeprecation
		@app.on_event("startup")
		def start_queue_processor():
			threading.Thread(target=self.cache_monitor, daemon=True).start()

		uvicorn.run(app, host="127.0.0.1", port=self.port)

	def process_requests(self, dbname: str):
		tasks = self.tasks.get(dbname)
		while True:
			task, args, result = tasks.get()
			try:
				if asyncio.iscoroutinefunction(task):
					val = asyncio.run(task(*args))
					print("async val", val)
					result.put(val)
				else:
					val = task(*args)
					print("sync val", val)
					result.put(val)
			except Exception:
				tasks.put(None)
			finally:
				tasks.task_done()

	def cache_monitor(self):
		while True:
			print("start cache checking...")
			now = int(time.time())
			instances = PetCollection.instances()
			for path in list(instances.keys()):
				dbname = os.path.relpath(path, STORAGE_PATH).split(os.sep)[0]
				print(f"check {dbname}.{instances[path]["instance"].name}...")
				if now - instances[path]["created"] > 3 * 24 * 3600:
					result = Queue(maxsize=1)
					self.tasks.get(dbname).put((self.clear_cache, (instances, path), result))
					return result.get()
			time.sleep(24 * 3600)

	def clear_cache(self, instances: dict[str, dict], path: str):
		print(f"clear {instances[path]["instance"].name}")
		del instances[path]
