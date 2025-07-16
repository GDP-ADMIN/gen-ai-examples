# previous notes

### step 1 - Development:
di dalam zip pipline yg akan di upload, list file yg mandatory:
1. pipeline.py
2. config.yaml

#### Notes
- Kalau type di extra config nya env, dia bakal encrypted
```yaml
extra_configs:
  - name: mcp_server_url
    type: env
    ui_type: text_field
    level: PRESET
```

- Ketika kita bikin pipeline, semua variable harus di masukin di:
```py
class McpPresetConfig(BasePipelinePresetConfig):
    """A Pydantic model representing the preset config of a simple pipeline.

    Inherits attributes from `BasePipelinePresetConfig`.
    """

    mcp_server_url: str
```

- Semua step di dalam component pipeline yang butuh `runtime_config_map`, itu masuknya di `additional_config_class = StandardRAGRuntimeConfig`

### step 2 - How to Upload:
- Di upload secara UI di gllm-backend
- Harus serve di local
- Bisa di upload di gl-chat staging
- Kita set values dari environment variable

### step 3 - How to Test:
Tembak curl ke chatbot_id yg kita configure di config.yml waktu kita upload zip atau sesuai yg kita isi kalau kita ngak nge set chatbots di config.yaml

---

# Questions

1. in `claudia_gpt/query_transformer/abbreviation/abbreviation_config_loader.py`, I want to query to database, ini bisa kah lgs pakai datastore? ke table tertentu, atau mending, atau mending di store nya as a file json?

di bagian:
```
agents = self._database.find_all(Table.AGENTS.value, {})
agent_type_map = {agent["id"]: agent["type"] for agent in agents}
```
2. kenapa variable ini: `normal_search_top_k`, itu ada di `additional_config_class` dan `preset_config_class`.
contoh: di files:
- `gdplabs_gen_ai_starter_gllm_backend/config/pipeline/standard_rag/preset_config.py`
- `gdplabs_gen_ai_starter_gllm_backend/config/pipeline/standard_rag/runtime_config.py`

Perbedaan antara `preset_config_class` dan `additional_config_class` adalah:
- `additional_config_class` idealnya digunakan ketika runtime

3. Untuk logger, ini kita bisa pasang nya seperti apa ya? apakah bisa pakai object logger yg di define oleh glchat? atau kita bikin object logger terpisah? atau sementara pakai print dulu?

4. kalau penggunaan seperti ini:
```py
self.data_store = SQLAlchemySQLDataStore(engine_or_url=os.getenv("GLCHAT_DB_URL"), pool_pre_ping=True)
```

dengan statement sebelumnya, hasil dari `os.getenv("GLCHAT_DB_URL")` akan menghasilkan environment variable yang ada suffix preset id, bukan value dari glchat db url. apakah ini betul?
atau memang ini expected karena ada beberapa env variable yang perlakuannya berbeda?

maksudnya adalah, hanya environment variable yang dari external saja yang perlakuannya:
instead of dapat value nya, akan dapat key dari env variable tersebut.

5. Di `claudia_gpt/config/constant.py`, saya ada beberapa constant yang ambil dari env variable. apakah kita bisa menggunakan metode seperti ini? (seharusnya kalau dari penjelasan kak Ryan mengenai hasil dari `os.getenv("COHERE_API_KEY", "")` itu bukan value nya tetapi key yang sudha di suffix), berarti kita tidak bisa menggunakan metode config/constant.py.

sehingga metode ini harus direfactor dengan cara:
1. semua env variable yang mau saya masukkan pertama harus di register di `config.yaml`
2. semua env variable baru tersebut harus saya masukkan kedalam `preset_config_class = ClaudiaPresetConfig`
3. kita hanya bisa menarik value dari env variable hanya melalui function `async def build(self, pipeline_config: dict[str, Any])` di dalam `claudia_gpt/pipeline.py`, sehingga ketika ada file lain yang membutuhkan env variable ini, mau tidak mau kita harus passing via parameter (salah satu caranya).

---

# Answer

1. mestinya bisa langsung pake datastore
   - oke noted buat yang ini
2. betul, yg runtime buat dipake lewat runtime config map itu
   - untuk yang no 2 ini, lebih ke, apa ngak bisa dibikin salah satu aja? antara di `additional_config_class` atau di `preset_config_class`
3. dari diskusi kmrn2, custom pipeline mestinya ga boleh pake component gl chat (kecuali dipindah ke gllm plugin), tapi gw lupa logger gl chat itu pake sdk atau ada custom nya lagi ya
   - berarti untuk yang ini, kita pakai print dulu sementara aja ya?
4. nah iya soal env ini jadi ada 2 macem : yg udah ada di gl chat dan yg blm. kalo yg udah ada jadinya ga perlu masukin preset config, bisa langsung di get dan key nya as is. kalo yg blm, baru perlu dimasukin preset config, dan key nya kita add suffix preset uuidnya, supaya beda preset ga nabrak value env nya
   - untuk yg ini gimana cara kita tau list of enviroinment variable apa aja yang punya GLCHAT dan mana yang blum punya GLCHAT
5. kalo env var yg ada di gl chat: bisa. tapi kalo blm, ga bisa. mungkin bedanya itu apakah nanti GL chat BE buat claudia itu khusus claudia aja: bisa tambahin aja env var nya di BE nya. kalo claudia pipeline dimasukin ke GL chat BE yg existing skrg: ga bisa, kecuali GL chat masukin env var khusus claudia dulu
   - untuk yang ini, better kita masukin semua nya lewat config.yaml dan dimasukin di `preset_config_class` aja ya?
