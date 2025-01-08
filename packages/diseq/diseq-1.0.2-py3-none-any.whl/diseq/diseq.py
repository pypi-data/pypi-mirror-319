import pickle
from datetime import datetime
import json
import pandas as pd
import requests
import torch
from gensim.models import Word2Vec
from langchain_community.embeddings.ollama import OllamaEmbeddings
from scipy.spatial import distance
from sklearn.decomposition import PCA
from tabulate import tabulate
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModel
import os
import gdown


class Diseq:
    def __init__(self):
        self.diseases = None
        self.disease_df = None
        self.disease2data = None
        self.node2vec_model = None
        self.llm_model = None
        self.description_device = None
        self.description_tokenizer = None
        self.description_model = None
        self.synonym_device = None
        self.synonym_tokenizer = None
        self.synonym_model = None
        self.do_pca = None
        self.pca_dimensions = None
        self.pca_matrices = None
        self.compounds = None
        self.data_dir = None

        log("If not done yet, please first use the download_data function!")
        log("Then use the init_tool function")


    def init_tool(self, data_dir, username, password, do_pca=False, pca_dimensions=100):
        log("Initialising tool..")
        synonym_model_name = "microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext"
        description_model_name = "michiyasunaga/BioLinkBERT-large"

        path_embeddings = os.path.join(data_dir, "embeddings.pickle")
        path_diseases = os.path.join(data_dir, "diseases.pickle")
        path_node2vec_model = os.path.join(data_dir, "node2vec_gene_model")


        # init embeddings
        with open(path_diseases, "rb") as handle:
            self.disease_df = pickle.load(handle)
            self.diseases = set(self.disease_df['ID'])

        #with open(path_embeddings, "rb") as handle:
        #    self.disease2embeddings = pickle.load(handle)

        self.compounds = ['Label', 'Description', 'Synonyms', 'Genes']
        self.pca_matrices = []
        self.pca_dimensions = pca_dimensions
        self.do_pca = do_pca

        # init models for query embedding
        self.synonym_model, self.synonym_tokenizer, self.synonym_device = init_huggingface_model(
            synonym_model_name)
        self.description_model, self.description_tokenizer, self.description_device = init_huggingface_model(
            description_model_name)
        self.llm_model = init_llm_model("gemma2:9b", username, password)
        self.node2vec_model = init_node2vec_gene_model(path_node2vec_model)
        self.disease2data = self.disease_df.set_index('ID').T.to_dict('list')

        if do_pca:
            log(f"Doing PCA on compounds to {pca_dimensions} dimensions")
            pca_embeddings = []
            for index, compound in tqdm(enumerate(self.compounds), total=len(self.compounds)):
                emb, pca_matrix = pca_compound(self.disease2embeddings, index, pca_dimensions)
                pca_embeddings.append(emb)
                self.pca_matrices.append(pca_matrix)

            keys = list(self.disease2embeddings.keys())
            disease2pca_embedding = {}
            for i in range(len(keys)):
                disease_id = keys[i]
                label_embedding = pca_embeddings[0][i]
                description_embedding = pca_embeddings[1][i]
                synonym_embedding = pca_embeddings[2][i]
                gene_embedding = pca_embeddings[3][i]
                # phenotype_embedding = pca_embeddings[4][i]
                disease2pca_embedding[disease_id] = [label_embedding, description_embedding, synonym_embedding,
                                                     gene_embedding]  # , phenotype_embedding]

            self.disease2embeddings = disease2pca_embedding

        log("Tool initialized!")

    def download_data(self, data_dir):
        self.data_dir = data_dir
        log("Starting downloads..")
        URL_EMBEDDINGS = "https://drive.google.com/uc?id=10Qz5dLyVj9S8n0prEEDuEf0EYIAh7-fG"
        URL_DISEASES = "https://drive.google.com/uc?id=1E0CYr3f1F55KF1bVbxkLB22Kd_2pGiUP"
        URL_NODE2VEC = "https://drive.google.com/uc?id=1SyiLB2uimJ2MqPU8f7SsLrhMw4xVkcgI"

        #EMBEDDINGS_PATH = os.path.join(data_dir, "embeddings.pickle")
        DISEASES_PATH = os.path.join(data_dir, "diseases.pickle")
        NODE2VEC_PATH = os.path.join(data_dir, "node2vec_gene_model")

        #gdown.download(URL_EMBEDDINGS, EMBEDDINGS_PATH)
        gdown.download(URL_DISEASES, DISEASES_PATH)
        gdown.download(URL_NODE2VEC, NODE2VEC_PATH)

        log(f"Done!Data saved in {data_dir}")
        log("Please use ")

    def query_embedding_space(self, query):
        # embed query
        query_embedding = self._embed_query(query)
        if self.do_pca:
            query_embedding = pca_query(query_embedding, self.pca_dimensions, self.pca_matrices)
        databases = []
        disease_ids = []
        distances = []
        labels = []
        descriptions = []
        synonyms = []
        genes = []
        for disease_id, embeddings in tqdm(self.disease2embeddings.items(), total=len(self.disease2embeddings)):
            dist = calculate_embedding_distance(query_embedding, self.disease2embeddings[disease_id])
            if dist != -1 and disease_id in self.disease2data:
                label, description, cur_synonyms, cur_genes, _ = self.disease2data[disease_id]
                databases.append(disease_id.split(":")[0])
                disease_ids.append(disease_id)
                distances.append(dist)
                labels.append(label)
                descriptions.append(description)
                synonyms.append(cur_synonyms)
                genes.append(cur_genes)

        df = pd.DataFrame({
            "Database": databases,
            "ID": disease_ids,
            "Distance": distances,
            "Label": labels,
            "Description": descriptions,
            "Synonyms": synonyms,
            "Genes": genes
        })

        self.available_databases = set(databases)

        return df

    def show_closest_diseases(self, df, top_k=5, databases='All', annotations='All', word_limit=10):
        # databases and annotations can be a list of databases -> check if all given are valid
        if databases != 'All':
            for db in databases:
                if db not in self.available_databases:
                    raise ValueError(
                        f"Database '{db}' is not available. Available databases are: {', '.join(self.available_databases)}")
        if annotations != "All":
            for an in annotations:
                if an not in self.compounds:
                    raise ValueError(
                        f"Annotation '{an}' is not available. Available annotations are: {', '.join(self.compounds)}")

        # filter df accordingly
        if databases != 'All':
            df = df[df['Database'].isin(databases)]

        if annotations != 'All':
            display_columns = ['ID', 'Distance'] + annotations
        else:
            display_columns = df.columns.drop('Database')

        if 'Genes' in df.columns:
            df['Genes'] = df['Genes'].apply(clean_genes)

        if 'Description' in df.columns:
            df['Description'] = df['Description'].apply(truncate_text, word_limit=word_limit)

        if 'Synonyms' in df.columns:
            df['Synonyms'] = df['Synonyms'].apply(truncate_text, word_limit=word_limit)

        results = {}

        # Group by Database and sort by Distance, then take the top_k diseases for each database
        grouped = df.groupby('Database')
        for db, group in grouped:
            top_k_diseases = group.nsmallest(top_k, 'Distance')
            results[db] = top_k_diseases[display_columns]

        # Print out the results in a nice format using tabulate
        for db, table in results.items():
            print(f"\nTop {top_k} diseases for database: {db}")
            print(tabulate(table, headers='keys', tablefmt='fancy_grid', maxcolwidths=25))

    def save_label_embeddings_to_file(self, path):
        output = ["id\tlabel\tembedding"]
        for disease_id, emb in self.disease2embeddings.items():
            label = self.disease2data[disease_id][0]
            label_emb = emb[0]
            output.append(f"{disease_id}\t{label}\t{label_emb}")

        with open(path, "w") as out:
            out.write("\n".join(output))

    def embed_label(self, label):
        raw_embedding = embed_llm(self.llm_model, label)
        if self.do_pca:
            return pca_query([raw_embedding], self.pca_dimensions, self.pca_matrices)
        else:
            return raw_embedding

    def _embed_query(self, query):
        query_embedding = []
        llm_dimensions = len(self.llm_model.embed_query("test"))

        if "Label" in query and len(query['Label']) > 2:
            query_embedding.append(self.llm_model.embed_documents([query['Label']])[0])
        else:
            query_embedding.append(np.zeros(llm_dimensions))

        if "Description" in query and len(query['Description']) > 2:
            query_embedding.append(embed_huggingface(self.description_model, self.description_tokenizer,
                                                     self.description_device, query['Description']))
        else:
            query_embedding.append(np.zeros(llm_dimensions))

        if "Synonyms" in query and len(query['Synonyms']) > 2:
            query_embedding.append(embed_huggingface(self.synonym_model, self.synonym_tokenizer,
                                                     self.synonym_device, query['Synonyms']))
        else:
            query_embedding.append(np.zeros(5))

        if "Genes" in query and len(query['Genes']) > 0:
            query_embedding.append(embed_node2vec(self.node2vec_model, query['Genes']))
        else:
            query_embedding.append(np.zeros(self.node2vec_model.vector_size))

        return query_embedding


def calculate_embedding_distance(emb1, emb2, compounds=[0, 1, 2, 3]):
    distances = []
    cur_compound = 0
    for e1, e2 in zip(emb1, emb2):
        if cur_compound in compounds:
            if not np.all(e1 == 0) and not np.all(e2 == 0):
                dist = distance.cosine(e1, e2)
                distances.append(dist)

        cur_compound += 1

    if len(distances) > 0:
        return np.mean(distances)
    else:
        return -1


def log(message):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")


def embed_node2vec(model, genes):
    keyword_embeddings = [model.wv[keyword] for keyword in genes if keyword in model.wv]
    if keyword_embeddings:
        embeddings = np.mean(keyword_embeddings, axis=0)  # todo: mean macht vll alles kaput??
    else:
        embeddings = np.zeros(model.vector_size)

    return np.squeeze(embeddings)


def embed_llm(model, text):
    return model.embed_documents([text])[0]
    #return model.embed_query(text)


def embed_huggingface(model, tokenizer, device, text):
    inputs = tokenizer([text], return_tensors="pt", max_length=512, truncation=True, padding=True)
    inputs = {name: tensor.to(device) for name, tensor in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = np.squeeze(outputs.last_hidden_state[:, 0, :].cpu().numpy())

    return embeddings


def init_huggingface_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()
    return model, tokenizer, device


def init_llm_model(model_name, username, password):
    protocol = "https"
    hostname = "chat.cosy.bio"

    host = f"{protocol}://{hostname}"

    auth_url = f"{host}/api/v1/auths/signin"
    api_url = f"{host}/ollama"

    account = {'email': username, 'password': password}
    auth_response = requests.post(auth_url, json=account)

    if auth_response.status_code != 200:
        raise ValueError(f"Authentication failed: {auth_response.status_code} - {auth_response.text}")
    else:
        log("Auth successful!")

    jwt = json.loads(auth_response.text)["token"]

    embedder = OllamaEmbeddings(base_url=api_url, model=model_name, headers={"Authorization": "Bearer " + jwt})

    return embedder


def init_node2vec_gene_model(path):
    model = Word2Vec.load(path)
    return model


def pca_query(embeddings, dimensions, pca_matrices):
    pca_emb = []
    for compound_ind, compound_emb in enumerate(embeddings):
        embedding_dimensions = len(compound_emb)
        pca = pca_matrices[compound_ind]
        if np.all(compound_emb == 0):
            pca_emb.append(np.zeros(dimensions))
        else:
            if embedding_dimensions <= dimensions:
                pca_emb.append(compound_emb)
            else:
                v = pca.transform([compound_emb])
                pca_emb.append(np.squeeze(v))
    return pca_emb


def pca_compound(disease2embeddings, compound_index, dimensions):
    # pretty complicated because of zero vectors (if database didnt provide the compound)
    # apply pca only on non-zero vectors -> rebuild the embedding space

    final_embeddings = []
    pca_matrix = None

    embedding_dimensions = len(disease2embeddings[list(disease2embeddings.keys())[0]][compound_index])

    if embedding_dimensions <= dimensions:
        final_embeddings = [embedding[compound_index] for embedding in disease2embeddings.values()]

    else:
        non_zero_embeddings = []
        zero_indices = []
        for i, embedding in enumerate(disease2embeddings.values()):
            if np.all(embedding[compound_index] == 0):
                zero_indices.append(i)
            else:
                non_zero_embeddings.append(embedding[compound_index])

        pca = PCA(n_components=dimensions)
        pca.fit(non_zero_embeddings)
        pca_matrix = pca
        reduced_embeddings = pca.transform(non_zero_embeddings)

        non_zero_index = 0
        zero_vector = np.zeros(dimensions)

        for i in range(len(disease2embeddings.values())):
            if i in zero_indices:
                final_embeddings.append(zero_vector)
            else:
                final_embeddings.append(reduced_embeddings[non_zero_index])
                non_zero_index += 1

    return final_embeddings, pca_matrix

def clean_genes(genes):
    if isinstance(genes, list):
        # Return an empty string if the list is empty or contains only empty strings
        cleaned_genes = [gene for gene in genes if gene]
        return '' if not cleaned_genes else cleaned_genes
    return genes  # Return as-is if not a list


def truncate_text(text, word_limit=6):
    words = text.split()
    if len(words) > word_limit:
        return ' '.join(words[:word_limit]) + '...'
    return text
