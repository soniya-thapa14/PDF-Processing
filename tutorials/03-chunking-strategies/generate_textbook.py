"""Generate a ~45 page educational PDF about Embeddings and Large Language Models."""

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak


OUTPUT_PATH = Path(__file__).parent / "pdfs" / "research_textbook.pdf"


def get_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='ChapterTitle',
        parent=styles['Heading1'],
        fontSize=22,
        spaceAfter=30,
        spaceBefore=40,
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        name='SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
    ))
    styles.add(ParagraphStyle(
        name='SubSection',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=10,
        spaceBefore=14,
    ))
    styles.add(ParagraphStyle(
        name='BodyProse',
        parent=styles['BodyText'],
        fontSize=11,
        leading=16,
        spaceAfter=14,
        alignment=TA_JUSTIFY,
    ))
    styles.add(ParagraphStyle(
        name='MathBlock',
        parent=styles['BodyText'],
        fontSize=11,
        leading=16,
        leftIndent=30,
        rightIndent=30,
        spaceAfter=12,
        spaceBefore=12,
        fontName='Courier',
    ))
    styles.add(ParagraphStyle(
        name='RefStyle',
        parent=styles['BodyText'],
        fontSize=10,
        leading=14,
        spaceAfter=8,
        fontName='Times-Italic',
    ))
    return styles


def build_title_page(story, styles):
    story.append(Spacer(1, 4 * cm))
    story.append(Paragraph("Embeddings and Large Language Models", styles['Title']))
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph("A Comprehensive Introduction to Modern NLP", styles['Heading2']))
    story.append(Spacer(1, 2 * cm))
    story.append(Paragraph(
        "From Word Vectors to Generative Pre-trained Transformers",
        styles['Heading3']
    ))
    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph("Part I: Embeddings (Chapters 1-4)", styles['BodyProse']))
    story.append(Paragraph("Part II: Large Language Models (Chapters 5-8)", styles['BodyProse']))
    story.append(PageBreak())


def build_chapter1(story, styles):
    story.append(Paragraph("Chapter 1: What Are Embeddings?", styles['ChapterTitle']))
    story.append(Paragraph("1.1 Definition and Motivation", styles['SectionTitle']))
    story.append(Paragraph(
        "An embedding is a mapping from discrete objects\u2014such as words, sentences, or entire "
        "documents\u2014into a continuous vector space. More precisely, an embedding function "
        "f: X \u2192 R^d maps each element of a discrete set X to a point in d-dimensional "
        "Euclidean space. The key property that makes embeddings useful is that semantically "
        "similar objects are mapped to nearby points in this space, while dissimilar objects "
        "are mapped to distant points.", styles['BodyProse']))
    story.append(Paragraph(
        "The concept of representing symbolic data as continuous vectors is fundamental to "
        "modern machine learning. Neural networks operate on continuous-valued inputs and "
        "produce continuous-valued outputs through differentiable operations. Since many "
        "real-world data types\u2014words, categorical variables, graph nodes, molecular "
        "structures\u2014are inherently discrete, we need a bridge between the discrete world "
        "and the continuous world of neural computation. Embeddings provide this bridge.", styles['BodyProse']))
    story.append(Paragraph(
        "Consider the task of representing the meaning of English words for a computer. "
        "A vocabulary of 100,000 words presents an immediate challenge: how do we encode "
        "each word so that a machine learning model can reason about semantic relationships? "
        "The naive approach of assigning each word an integer index (cat=1, dog=2, house=3) "
        "imposes an arbitrary ordering that has no semantic significance. The distance between "
        "indices tells us nothing about the relationship between words.", styles['BodyProse']))
    story.append(Paragraph(
        "Embeddings solve this problem by learning a function that maps each word to a dense "
        "vector in a continuous space where geometric proximity reflects semantic similarity. "
        "The word 'cat' might be mapped to a 300-dimensional vector that is close to 'kitten' "
        "and 'feline' but far from 'automobile' and 'democracy'. This is not hand-engineered; "
        "it emerges automatically from training on large text corpora.", styles['BodyProse']))

    story.append(Paragraph("1.2 The Distributional Hypothesis", styles['SectionTitle']))
    story.append(Paragraph(
        "The theoretical foundation for word embeddings comes from the distributional "
        "hypothesis, most famously articulated by the British linguist J.R. Firth in 1957: "
        "\"You shall know a word by the company it keeps.\" This principle states that words "
        "appearing in similar linguistic contexts tend to have similar meanings. For example, "
        "the words 'dog' and 'cat' frequently appear in similar contexts ('The ___ sat on "
        "the mat', 'She fed the ___', 'The ___ was sleeping'), which suggests they share "
        "semantic properties (both are common household pets, both are animate beings).", styles['BodyProse']))
    story.append(Paragraph(
        "The distributional hypothesis was developed further by linguists such as Zellig Harris "
        "(1954) and later formalized in computational linguistics through methods like Latent "
        "Semantic Analysis (Deerwester et al., 1990). The core insight\u2014that meaning can be "
        "derived from patterns of co-occurrence\u2014underlies virtually all modern embedding "
        "methods, from Word2Vec to the contextual representations produced by large language models.", styles['BodyProse']))
    story.append(Paragraph(
        "This hypothesis has profound implications for natural language processing. It suggests "
        "that we do not need to manually encode the meaning of words through hand-crafted features "
        "or ontologies. Instead, we can learn meaning automatically from large corpora of text by "
        "observing statistical patterns of word usage. A word's meaning is emergent from its "
        "distribution across contexts, and this distribution can be captured efficiently in a "
        "dense vector representation.", styles['BodyProse']))

    story.append(Paragraph("1.3 One-Hot Encoding and Its Limitations", styles['SectionTitle']))
    story.append(Paragraph(
        "Before embeddings became widespread, most NLP systems relied on symbolic representations "
        "where each word was treated as an atomic, indivisible unit with no internal structure. "
        "The most common formalization of this approach is one-hot encoding, which has historical "
        "roots in information theory and digital communication systems.", styles['BodyProse']))
    story.append(Paragraph(
        "The simplest representation for categorical data is one-hot encoding. Given a vocabulary "
        "of V words, each word is represented as a binary vector of length V with exactly one "
        "element set to 1 and all others set to 0. For example, in a vocabulary of 50,000 words, "
        "the word 'cat' might be represented as a vector with a 1 in position 4,217 and zeros "
        "everywhere else.", styles['BodyProse']))
    story.append(Paragraph(
        "One-hot encoding has three critical limitations. First, the vectors are extremely sparse: "
        "a vocabulary of 100,000 words produces 100,000-dimensional vectors where 99.999% of "
        "the values are zero. This is computationally wasteful and memory-intensive. Second, all "
        "one-hot vectors are orthogonal to each other\u2014the dot product of any two distinct "
        "one-hot vectors is exactly zero. This means the representation encodes no information "
        "about word similarity: the distance between 'cat' and 'dog' is identical to the distance "
        "between 'cat' and 'refrigerator'.", styles['BodyProse']))
    story.append(Paragraph(
        "Third, one-hot vectors suffer from the curse of dimensionality. As the vocabulary grows, "
        "the dimensionality of the representation grows linearly, making storage and computation "
        "increasingly expensive. Furthermore, one-hot representations do not generalize: learning "
        "that 'cat' appears in certain contexts provides no information about 'kitten' or 'feline' "
        "because their representations share no structure.", styles['BodyProse']))

    story.append(Paragraph("1.4 Dense Representations", styles['SectionTitle']))
    story.append(Paragraph(
        "Dense embeddings solve these problems by representing each word as a relatively "
        "low-dimensional vector (typically 100 to 768 dimensions) where every component can "
        "take any real value. In a 300-dimensional embedding space, each word is a point in "
        "R^300, and the geometric relationships between points encode semantic relationships "
        "between words. Words with similar meanings cluster together; words with different "
        "meanings are distant.", styles['BodyProse']))
    story.append(Paragraph(
        "The advantages of dense representations are substantial. Storage is reduced by orders "
        "of magnitude: a 300-dimensional float vector requires 1,200 bytes, compared to 400,000 "
        "bytes for a one-hot vector over a 100,000-word vocabulary. Computation is faster because "
        "dense matrix operations are highly optimized on modern hardware (GPUs, TPUs). Most "
        "importantly, the continuous nature of the space allows the model to generalize: if "
        "'cat' and 'kitten' have similar embeddings, any function learned for 'cat' will "
        "naturally transfer to 'kitten' without additional training examples.", styles['BodyProse']))
    story.append(Paragraph(
        "Dense embeddings also enable meaningful mathematical operations on word meanings. The "
        "most famous example is vector arithmetic: the relationship 'king - man + woman' "
        "produces a vector close to 'queen'. This suggests that the embedding space has learned "
        "to encode abstract relationships like gender as consistent directional offsets. Such "
        "structure emerges automatically from training on large text corpora, without any "
        "explicit supervision about gender or royalty.", styles['BodyProse']))

    story.append(Paragraph("1.5 Types of Embeddings", styles['SectionTitle']))
    story.append(Paragraph(
        "Embeddings come in several varieties depending on the granularity of the input and "
        "whether context is considered. Word embeddings (Word2Vec, GloVe) assign a single fixed "
        "vector to each word in the vocabulary. These are context-independent: the word 'bank' "
        "always receives the same vector regardless of whether it appears in 'river bank' or "
        "'bank account'. Subword embeddings (FastText) extend word embeddings by representing "
        "each word as a sum of its character n-gram vectors, enabling representations for "
        "out-of-vocabulary words through morphological composition.", styles['BodyProse']))
    story.append(Paragraph(
        "Contextual embeddings (ELMo, BERT) produce different vectors for the same word depending "
        "on its surrounding context. The word 'bank' in 'I deposited money at the bank' receives "
        "a different vector than in 'I sat by the river bank'. Sentence embeddings (Sentence-BERT, "
        "Universal Sentence Encoder) map entire sentences to single vectors, enabling comparison "
        "of sentence-level meaning. Document embeddings extend this to entire passages or articles. "
        "Each level of granularity serves different applications: word embeddings for lexical "
        "analysis, sentence embeddings for semantic search, document embeddings for clustering.", styles['BodyProse']))
    story.append(Paragraph(
        "Beyond text, embeddings are used in many other domains. Image embeddings from models "
        "like CLIP map images to vectors in the same space as text, enabling cross-modal "
        "retrieval (searching for images using text queries). Graph embeddings (Node2Vec, "
        "GraphSAGE) represent nodes in a graph as vectors that preserve graph structure. "
        "Protein embeddings (ESM) represent amino acid sequences as vectors for predicting "
        "protein function. Audio embeddings represent speech or music for retrieval and "
        "classification. The unifying principle across all these domains is the same: map "
        "discrete or complex structured data into a continuous space where geometric "
        "relationships encode meaningful similarities.", styles['BodyProse']))
    story.append(PageBreak())


def build_chapter2(story, styles):
    story.append(Paragraph("Chapter 2: The Mathematics of Embeddings", styles['ChapterTitle']))
    story.append(Paragraph("2.1 Vector Spaces and Linear Algebra Foundations", styles['SectionTitle']))
    story.append(Paragraph(
        "To understand embeddings rigorously, we need the language of linear algebra. A vector "
        "space over the real numbers R is a set V equipped with two operations\u2014vector addition "
        "and scalar multiplication\u2014satisfying axioms of closure, associativity, commutativity, "
        "identity elements, and distributivity. The most common vector space in machine learning "
        "is R^d, the set of all d-tuples of real numbers.", styles['BodyProse']))
    story.append(Paragraph(
        "Each embedding vector v in R^d can be written as v = (v_1, v_2, ..., v_d), where each "
        "component v_i is a real number. The norm (or length) of a vector is defined as "
        "||v|| = sqrt(v_1^2 + v_2^2 + ... + v_d^2), which is the Euclidean distance from the "
        "origin to the point v. A unit vector has norm 1 and represents a pure direction in space.", styles['BodyProse']))
    story.append(Paragraph(
        "The concept of a basis is central to understanding embedding spaces. A basis for R^d "
        "is a set of d linearly independent vectors that span the entire space. Any vector can "
        "be written as a unique linear combination of basis vectors. While the standard basis "
        "consists of one-hot vectors (e_1, e_2, ..., e_d), learned embeddings typically do not "
        "align with any interpretable basis\u2014the meaning is distributed across all dimensions.", styles['BodyProse']))

    story.append(Paragraph("2.2 Dot Product and Its Interpretation", styles['SectionTitle']))
    story.append(Paragraph(
        "The dot product (or inner product) of two vectors a and b in R^d is defined as:",
        styles['BodyProse']))
    story.append(Paragraph(
        "a . b = sum(a_i * b_i) for i = 1 to d = a_1*b_1 + a_2*b_2 + ... + a_d*b_d",
        styles['MathBlock']))
    story.append(Paragraph(
        "The dot product has a geometric interpretation: a . b = ||a|| * ||b|| * cos(theta), "
        "where theta is the angle between the two vectors. When both vectors point in similar "
        "directions (theta close to 0), the dot product is large and positive. When they are "
        "orthogonal (theta = 90 degrees), the dot product is zero. When they point in opposite "
        "directions (theta close to 180 degrees), the dot product is large and negative.", styles['BodyProse']))
    story.append(Paragraph(
        "In the context of embeddings, the dot product measures the degree of alignment between "
        "two word vectors. A high dot product indicates that two words share similar semantic "
        "properties. However, the dot product is sensitive to vector magnitude: longer vectors "
        "will tend to have larger dot products regardless of their direction. This can be "
        "problematic when comparing words that differ in frequency.", styles['BodyProse']))

    story.append(Paragraph("2.3 Cosine Similarity", styles['SectionTitle']))
    story.append(Paragraph(
        "Cosine similarity addresses the magnitude sensitivity of the dot product by normalizing "
        "each vector to unit length before computing the inner product:",
        styles['BodyProse']))
    story.append(Paragraph(
        "cos(theta) = (a . b) / (||a|| * ||b||)",
        styles['MathBlock']))
    story.append(Paragraph(
        "The result is always between -1 and 1. A cosine similarity of 1 means the vectors "
        "point in exactly the same direction (regardless of magnitude), 0 means they are "
        "orthogonal, and -1 means they point in exactly opposite directions. This scale "
        "invariance makes cosine similarity the standard metric for comparing word embeddings.", styles['BodyProse']))
    story.append(Paragraph(
        "In practice, cosine similarity is used extensively in information retrieval and "
        "semantic search. To find documents most relevant to a query, we compute the cosine "
        "similarity between the query embedding and each document embedding, then rank by "
        "similarity. This approach works because documents about similar topics will have "
        "similar embedding directions, even if they differ in length or vocabulary richness.", styles['BodyProse']))

    story.append(Paragraph("2.4 Euclidean Distance vs. Cosine Similarity", styles['SectionTitle']))
    story.append(Paragraph(
        "Euclidean distance between two vectors a and b is defined as d(a,b) = ||a - b|| = "
        "sqrt(sum((a_i - b_i)^2)). Unlike cosine similarity, Euclidean distance considers "
        "both direction and magnitude. Two vectors can have high cosine similarity (same "
        "direction) but large Euclidean distance (different magnitudes).", styles['BodyProse']))
    story.append(Paragraph(
        "When to use which metric depends on the application. Cosine similarity is preferred "
        "when we care only about the topic or meaning of text, regardless of its length. "
        "Euclidean distance is preferred when magnitude carries information\u2014for example, "
        "when embedding vectors encode not just direction (topic) but also confidence. "
        "In practice, if embeddings are L2-normalized (projected onto the unit hypersphere), "
        "minimizing Euclidean distance is equivalent to maximizing cosine similarity.", styles['BodyProse']))

    story.append(Paragraph("2.5 Vector Arithmetic and Semantic Relationships", styles['SectionTitle']))
    story.append(Paragraph(
        "One of the most striking properties of well-trained word embeddings is that vector "
        "arithmetic captures semantic relationships. The canonical example, discovered by "
        "Mikolov et al. (2013), is:", styles['BodyProse']))
    story.append(Paragraph(
        "vector('king') - vector('man') + vector('woman') ~ vector('queen')",
        styles['MathBlock']))
    story.append(Paragraph(
        "This works because the embedding space encodes the gender relationship as a consistent "
        "directional offset. The vector from 'man' to 'woman' represents the concept of "
        "gender transformation, and this same offset applies to other gendered pairs: "
        "'uncle' to 'aunt', 'king' to 'queen', 'boy' to 'girl'. Similarly, country-capital "
        "relationships form consistent offsets: 'France' - 'Paris' + 'Berlin' produces a "
        "vector near 'Germany'.", styles['BodyProse']))
    story.append(Paragraph(
        "These analogies work because embedding models learn to encode multiple independent "
        "semantic dimensions as approximately orthogonal directions in the vector space. Gender, "
        "number (singular/plural), tense (past/present), and other linguistic properties each "
        "correspond to rough directions, and these directions compose linearly. The analogy task "
        "typically achieves 60-75% accuracy on benchmark datasets, demonstrating rich geometric "
        "structure that mirrors human semantic intuitions.", styles['BodyProse']))

    story.append(Paragraph("2.6 Dimensionality Considerations", styles['SectionTitle']))
    story.append(Paragraph(
        "Why do practical embedding models use 300 to 768 dimensions? The answer involves a "
        "trade-off between representational capacity and statistical efficiency. Too few "
        "dimensions (say, 10) cannot capture the full complexity of word meanings. Too many "
        "dimensions (say, 10,000) lead to overfitting: the model has enough capacity to "
        "memorize training data rather than learning generalizable patterns.", styles['BodyProse']))
    story.append(Paragraph(
        "The Johnson-Lindenstrauss lemma provides theoretical justification: any set of n "
        "points in high-dimensional space can be projected into O(log n / epsilon^2) dimensions "
        "while preserving pairwise distances within a factor of (1 +/- epsilon). For a vocabulary "
        "of 100,000 words with epsilon=0.1, this gives roughly 2000 dimensions as an upper bound. "
        "In practice, 300 dimensions (Word2Vec, GloVe) to 768 dimensions (BERT) provide an "
        "excellent trade-off between semantic richness and computational tractability.", styles['BodyProse']))

    story.append(Paragraph("2.7 Nearest Neighbor Search in Embedding Spaces", styles['SectionTitle']))
    story.append(Paragraph(
        "A fundamental operation on embeddings is nearest neighbor search: given a query vector, "
        "find the k most similar vectors in a database. Exact nearest neighbor search requires "
        "computing the distance between the query and every vector in the database, which is "
        "O(n*d) for n vectors of dimension d. For a database of 100 million vectors, this "
        "brute-force approach is too slow for real-time applications.", styles['BodyProse']))
    story.append(Paragraph(
        "Approximate Nearest Neighbor (ANN) algorithms trade a small amount of accuracy for "
        "dramatic speedups. Hierarchical Navigable Small World (HNSW) graphs, introduced by "
        "Malkov and Yashunin (2018), build a multi-layer graph structure where each node is "
        "connected to its nearest neighbors. Search starts at the top layer (coarse) and "
        "descends to lower layers (fine-grained), achieving O(log n) query time. HNSW is "
        "the default index type in popular vector databases like Qdrant, Milvus, and Weaviate.", styles['BodyProse']))
    story.append(Paragraph(
        "Inverted File Index (IVF) partitions the vector space into regions using k-means "
        "clustering, then searches only the most relevant regions during query time. Product "
        "Quantization (PQ) compresses vectors by splitting them into sub-vectors and quantizing "
        "each independently, reducing memory requirements by 10-100x with minimal accuracy loss. "
        "These techniques can be combined (IVF-PQ) to handle billion-scale vector databases on "
        "modest hardware.", styles['BodyProse']))

    story.append(Paragraph("2.8 Embedding Space Geometry and Isotropy", styles['SectionTitle']))
    story.append(Paragraph(
        "An important property of embedding spaces is isotropy: whether the vectors are uniformly "
        "distributed across all directions, or whether they cluster in a narrow cone. Research "
        "by Ethayarajh (2019) showed that contextual embeddings from BERT and GPT-2 are highly "
        "anisotropic\u2014most vectors occupy a narrow region of the space, and the average "
        "cosine similarity between random word pairs is surprisingly high (around 0.6 for upper "
        "layers of BERT, rather than the expected 0 for isotropic distributions).", styles['BodyProse']))
    story.append(Paragraph(
        "Anisotropy degrades the usefulness of cosine similarity because all vectors are already "
        "somewhat similar. Post-processing techniques can improve isotropy: whitening (normalizing "
        "the covariance matrix to the identity), mean centering (subtracting the mean vector), "
        "or using contrastive learning objectives that explicitly push random pairs apart. "
        "Models trained with contrastive objectives (like Sentence-BERT with in-batch negatives) "
        "tend to produce more isotropic embeddings that better utilize the full capacity of the "
        "vector space.", styles['BodyProse']))
    story.append(PageBreak())


def build_chapter3(story, styles):
    story.append(Paragraph("Chapter 3: Training Embedding Models", styles['ChapterTitle']))
    story.append(Paragraph("3.1 Word2Vec (Mikolov et al., 2013)", styles['SectionTitle']))
    story.append(Paragraph(
        "Word2Vec, introduced by Tomas Mikolov, Kai Chen, Greg Corrado, and Jeffrey Dean at "
        "Google in their 2013 paper 'Efficient Estimation of Word Representations in Vector "
        "Space' (presented at ICLR 2013 Workshop), represents a watershed moment in natural "
        "language processing. The paper demonstrated that simple neural network architectures "
        "trained on large amounts of text could produce word vectors capturing remarkably "
        "rich semantic and syntactic relationships.", styles['BodyProse']))
    story.append(Paragraph(
        "Word2Vec proposes two complementary architectures: Continuous Bag-of-Words (CBOW) and "
        "Skip-gram. In CBOW, the model predicts a target word given its surrounding context "
        "words. For example, given the context 'The ___ sat on the mat', the model learns to "
        "predict 'cat'. The input is the average (or sum) of the context word vectors, passed "
        "through a single linear projection to predict the center word. In Skip-gram, the "
        "architecture is reversed: given a center word, the model predicts each surrounding "
        "context word independently.", styles['BodyProse']))
    story.append(Paragraph(
        "The architecture is deliberately simple. The model consists of two weight matrices: "
        "an input embedding matrix W (V x d) and an output embedding matrix W' (d x V), where "
        "V is the vocabulary size and d is the embedding dimension. There is no non-linear "
        "activation function between these layers\u2014the hidden layer is simply a linear "
        "projection (equivalently, a lookup table). The output layer uses softmax to produce "
        "a probability distribution over the vocabulary.", styles['BodyProse']))
    story.append(Paragraph(
        "A critical optimization is negative sampling, introduced in the follow-up paper "
        "'Distributed Representations of Words and Phrases and their Compositionality' "
        "(Mikolov et al., NeurIPS 2013). Computing the full softmax over a vocabulary of "
        "100,000+ words at every training step is prohibitively expensive. Negative sampling "
        "reformulates the problem: instead of predicting the correct word among all vocabulary "
        "words, the model learns to distinguish the true context word from 5-20 randomly sampled "
        "negative words. This reduces computation from O(V) to O(k) per training example.", styles['BodyProse']))
    story.append(Paragraph(
        "The results were remarkable. Trained on a Google News corpus of approximately 1.6 "
        "billion words, Word2Vec produced 300-dimensional vectors for 3 million words and "
        "phrases in less than a day on a single machine. The resulting vectors exhibited "
        "the famous analogy property and achieved state-of-the-art results on word similarity "
        "benchmarks. The paper has accumulated over 40,000 citations. However, Word2Vec has a "
        "fundamental limitation: each word receives exactly one vector regardless of context. "
        "The word 'bank' has a single representation whether it refers to a financial "
        "institution or a river bank.", styles['BodyProse']))

    story.append(Paragraph("3.2 GloVe (Pennington, Socher, Manning, 2014)", styles['SectionTitle']))
    story.append(Paragraph(
        "GloVe (Global Vectors for Word Representation) was introduced by Jeffrey Pennington, "
        "Richard Socher, and Christopher Manning at Stanford University in their 2014 paper "
        "presented at EMNLP. GloVe addresses a theoretical gap in Word2Vec: while Word2Vec "
        "operates on local context windows, it does not explicitly leverage the global "
        "co-occurrence statistics of the corpus. GloVe combines the advantages of global matrix "
        "factorization methods (like LSA) and local context window methods (like Word2Vec).", styles['BodyProse']))
    story.append(Paragraph(
        "The key insight behind GloVe is that ratios of co-occurrence probabilities encode "
        "meaning more directly than raw probabilities. Consider two words: 'ice' and 'steam'. "
        "The probability P(solid|ice) is high while P(solid|steam) is low, giving a large ratio. "
        "Conversely, P(water|ice) and P(water|steam) are both high, giving a ratio near 1. "
        "These ratios distinguish the relevant aspects of word meaning more cleanly than "
        "absolute probabilities.", styles['BodyProse']))
    story.append(Paragraph(
        "GloVe's training objective is a weighted least-squares regression on the logarithm "
        "of word-word co-occurrence counts:", styles['BodyProse']))
    story.append(Paragraph(
        "w_i^T * w_j + b_i + b_j = log(X_ij)",
        styles['MathBlock']))
    story.append(Paragraph(
        "where X_ij is the number of times word j appears in the context of word i, and b_i, "
        "b_j are bias terms. A weighting function f(X_ij) prevents rare co-occurrences from "
        "dominating the loss. GloVe achieved 75% accuracy on the word analogy task and "
        "outperformed Word2Vec on several word similarity benchmarks.", styles['BodyProse']))
    story.append(Paragraph(
        "An important property of GloVe is that the distinction between 'word' and 'context' "
        "vectors vanishes in the objective function: both w_i and w_j play symmetric roles. "
        "The final word vectors are computed as the sum of the word and context vectors: "
        "v_final = w + w_context. GloVe was trained on corpora ranging from Wikipedia (6B "
        "tokens, producing 400K vocabulary vectors) to Common Crawl (840B tokens, producing "
        "2.2M vocabulary vectors). The pre-trained vectors were released publicly and became "
        "standard initialization for many NLP models throughout 2015-2018.", styles['BodyProse']))

    story.append(Paragraph("3.3 ELMo (Peters et al., 2018)", styles['SectionTitle']))
    story.append(Paragraph(
        "Embeddings from Language Models (ELMo), introduced by Matthew Peters and colleagues "
        "at the Allen Institute for AI in their 2018 NAACL paper 'Deep contextualized word "
        "representations', marked the transition from static to contextual embeddings. Unlike "
        "Word2Vec and GloVe, which assign a single fixed vector to each word, ELMo produces "
        "different representations for the same word depending on its surrounding sentence.", styles['BodyProse']))
    story.append(Paragraph(
        "The architecture consists of a character-level convolutional layer followed by a "
        "2-layer bidirectional LSTM. The forward LSTM reads left-to-right, building "
        "representations that incorporate information from preceding words. The backward LSTM "
        "reads right-to-left, incorporating following words. At each position, outputs of both "
        "directions are concatenated.", styles['BodyProse']))
    story.append(Paragraph(
        "ELMo's final word representation is a learned weighted combination of all LSTM layers. "
        "Different layers capture different types of information: lower layers capture syntax "
        "(part-of-speech, grammatical structure) while higher layers capture semantics (word "
        "sense, semantic role). ELMo was the first model to convincingly demonstrate that "
        "pre-trained representations could transfer to improve a wide range of downstream NLP "
        "tasks, improving state-of-the-art on six NLP benchmarks.", styles['BodyProse']))

    story.append(Paragraph("3.4 BERT Embeddings (Devlin et al., 2019)", styles['SectionTitle']))
    story.append(Paragraph(
        "BERT (Bidirectional Encoder Representations from Transformers) was introduced by Jacob "
        "Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova at Google AI Language in "
        "their 2019 NAACL paper. BERT produces contextual embeddings using the Transformer "
        "encoder architecture, enabling much deeper models and more effective capturing of "
        "long-range dependencies than LSTMs.", styles['BodyProse']))
    story.append(Paragraph(
        "BERT is pre-trained with two objectives: Masked Language Modeling (MLM) and Next "
        "Sentence Prediction (NSP). In MLM, 15% of input tokens are randomly masked, and the "
        "model must predict the original tokens from surrounding context. BERT-base has 12 "
        "Transformer layers, 768 hidden dimensions, 12 attention heads, and 110 million "
        "parameters. BERT-large scales to 24 layers, 1024 dimensions, 16 heads, and 340 "
        "million parameters.", styles['BodyProse']))
    story.append(Paragraph(
        "To extract fixed-size sentence embeddings from BERT, the standard approach uses the "
        "output of the special [CLS] token. However, research showed that [CLS] is suboptimal "
        "for semantic similarity tasks because it was trained for next sentence prediction. "
        "Mean pooling over all token outputs often produces better sentence embeddings.", styles['BodyProse']))

    story.append(Paragraph("3.5 Sentence-BERT (Reimers and Gurevych, 2019)", styles['SectionTitle']))
    story.append(Paragraph(
        "Sentence-BERT (SBERT) was introduced by Nils Reimers and Iryna Gurevych at UKP Lab, "
        "TU Darmstadt, in their 2019 EMNLP paper 'Sentence-BERT: Sentence Embeddings using "
        "Siamese BERT-Networks'. The paper addresses a critical scalability problem: using "
        "BERT directly for finding similar sentence pairs requires feeding both sentences "
        "simultaneously for cross-attention. For 10,000 sentences, finding the most similar "
        "pair requires approximately 50 million BERT inferences, taking about 65 hours.", styles['BodyProse']))
    story.append(Paragraph(
        "SBERT solves this by fine-tuning BERT in a Siamese (twin) network architecture. "
        "Two identical BERT models (sharing weights) independently encode two sentences. "
        "A pooling layer (mean pooling by default) reduces token-level output to a fixed-size "
        "sentence embedding. The model is fine-tuned on Natural Language Inference data using "
        "objectives that encourage similar sentences to have similar embeddings.", styles['BodyProse']))
    story.append(Paragraph(
        "The result is dramatic: instead of 65 hours for pairwise comparison, SBERT finds "
        "the most similar pair in about 5 seconds (embed all 10,000 sentences, then compute "
        "cosine similarities). Experiments showed MEAN pooling outperforms both CLS token "
        "extraction and MAX pooling. SBERT embeddings achieve state-of-the-art results on "
        "semantic textual similarity benchmarks while being orders of magnitude faster than "
        "cross-encoder approaches.", styles['BodyProse']))
    story.append(PageBreak())


def build_chapter4(story, styles):
    story.append(Paragraph("Chapter 4: Modern Embedding Models and Applications", styles['ChapterTitle']))
    story.append(Paragraph("4.1 Lightweight Distilled Models", styles['SectionTitle']))
    story.append(Paragraph(
        "The all-MiniLM-L6-v2 model, released by the Sentence-Transformers project, represents "
        "the state of practical embedding models optimized for deployment. It is a 6-layer "
        "distilled model producing 384-dimensional embeddings in approximately 80MB. Despite "
        "its small size, it achieves competitive performance on semantic similarity benchmarks, "
        "making it the default choice for production systems where latency and memory matter.", styles['BodyProse']))
    story.append(Paragraph(
        "The distillation process involves training a smaller student model to mimic the behavior "
        "of a larger teacher model. The student learns not just to match the teacher's final "
        "embeddings but to approximate its internal representations. This knowledge distillation "
        "approach, first proposed by Hinton et al. (2015), allows the student to achieve 85-95% "
        "of the teacher's quality at a fraction of the computational cost. For all-MiniLM-L6-v2, "
        "the teacher is a 12-layer model, and the student retains most of its semantic "
        "understanding while being twice as fast at inference.", styles['BodyProse']))

    story.append(Paragraph("4.2 Proprietary Embedding APIs", styles['SectionTitle']))
    story.append(Paragraph(
        "OpenAI offers the text-embedding-3 family, released in January 2024. The "
        "text-embedding-3-small model produces 1536-dimensional vectors optimized for "
        "cost-effectiveness, while text-embedding-3-large produces 3072-dimensional vectors "
        "for maximum quality. These models support Matryoshka Representation Learning, meaning "
        "embeddings can be truncated to lower dimensions (e.g., 256 or 512) with graceful "
        "degradation rather than catastrophic information loss.", styles['BodyProse']))
    story.append(Paragraph(
        "The concept of Matryoshka embeddings (named after Russian nesting dolls) was introduced "
        "by Kusupati et al. (2022) in 'Matryoshka Representation Learning'. The key idea is to "
        "train the model so that the first k dimensions of a d-dimensional embedding are "
        "themselves a valid k-dimensional embedding. This is achieved by adding auxiliary losses "
        "at multiple dimensionalities during training. Users can choose their dimension at "
        "inference time, trading quality for speed/storage without retraining.", styles['BodyProse']))

    story.append(Paragraph("4.3 Applications of Embeddings", styles['SectionTitle']))
    story.append(Paragraph(
        "Semantic search is the most prominent application. Unlike keyword-based search (which "
        "matches exact terms), semantic search finds documents that are conceptually relevant "
        "even if they use different words. A query about 'climate change effects on agriculture' "
        "can match documents about 'global warming impact on crop yields' because their "
        "embeddings are geometrically close despite minimal word overlap. This requires embedding "
        "both queries and documents into the same vector space, then finding nearest neighbors "
        "efficiently using approximate nearest neighbor (ANN) algorithms like HNSW or IVF.", styles['BodyProse']))
    story.append(Paragraph(
        "Retrieval-Augmented Generation (RAG) combines embeddings with large language models. "
        "A knowledge base is pre-embedded and stored in a vector database. When a user asks a "
        "question, it is embedded and used to retrieve relevant passages via similarity search. "
        "These passages are provided as context to a language model, which generates an answer "
        "grounded in the retrieved information. RAG reduces hallucination and enables the model "
        "to answer questions about private or recent information not in its training data.", styles['BodyProse']))
    story.append(Paragraph(
        "Clustering and classification are natural applications of embedding spaces. K-means "
        "clustering on document embeddings discovers topic groups without labeled data. A simple "
        "linear classifier trained on embeddings achieves strong text classification performance "
        "because the embedding space already captures semantic distinctions. Anomaly detection "
        "identifies outlier documents whose embeddings are far from any cluster center, useful "
        "for detecting novel content, spam, or data quality issues.", styles['BodyProse']))

    story.append(Paragraph("4.4 Evaluation: The MTEB Benchmark", styles['SectionTitle']))
    story.append(Paragraph(
        "The Massive Text Embedding Benchmark (MTEB), introduced by Muennighoff et al. (2023), "
        "provides a comprehensive evaluation framework across 8 task categories: Classification, "
        "Clustering, Pair Classification, Reranking, Retrieval, Semantic Textual Similarity, "
        "Summarization, and BitextMining. MTEB includes 58 datasets spanning 112 languages.", styles['BodyProse']))
    story.append(Paragraph(
        "MTEB revealed that no single model dominates all tasks: models optimized for retrieval "
        "may underperform on classification, and vice versa. Model size correlates with "
        "performance but with diminishing returns. The benchmark also showed that instruction-tuned "
        "embedding models (trained with task-specific prompts like 'Represent this sentence for "
        "retrieval:') can outperform general-purpose embeddings on specific tasks while "
        "maintaining competitive generalist performance.", styles['BodyProse']))
    story.append(Paragraph(
        "The MTEB leaderboard has accelerated progress in embedding model development. "
        "Researchers can compare models across standardized tasks, identify weaknesses, and "
        "focus improvement efforts. The leaderboard shows a clear trend toward multi-task models "
        "that perform well across all categories, driven by innovations in training data "
        "curation, contrastive learning objectives, and model architecture.", styles['BodyProse']))

    story.append(Paragraph("4.5 Vector Databases and Infrastructure", styles['SectionTitle']))
    story.append(Paragraph(
        "The practical deployment of embeddings at scale requires specialized infrastructure. "
        "Vector databases\u2014purpose-built systems for storing, indexing, and querying high-"
        "dimensional vectors\u2014have emerged as a critical component. Popular options include "
        "Pinecone (fully managed), Weaviate (open-source with hybrid search), Qdrant (Rust-based, "
        "high performance), Milvus (distributed, scalable), and pgvector (PostgreSQL extension "
        "for teams already using PostgreSQL).", styles['BodyProse']))
    story.append(Paragraph(
        "Vector databases provide several key capabilities beyond simple nearest neighbor search. "
        "Metadata filtering allows combining vector similarity with structured constraints "
        "(e.g., 'find similar documents published after 2023'). Multi-tenancy supports isolated "
        "vector spaces for different users or applications. Real-time indexing allows new vectors "
        "to be immediately searchable without rebuilding the entire index. Hybrid search combines "
        "dense vector similarity with traditional sparse retrieval (BM25) for improved recall.", styles['BodyProse']))
    story.append(Paragraph(
        "The embedding pipeline in a production system typically involves: (1) chunking documents "
        "into passages of appropriate size (typically 256-512 tokens), (2) embedding each chunk "
        "using a model like all-MiniLM-L6-v2 or text-embedding-3-small, (3) storing vectors with "
        "metadata in a vector database, (4) at query time, embedding the user query with the "
        "same model, (5) performing ANN search to retrieve the top-k most similar chunks, and "
        "(6) optionally re-ranking results with a cross-encoder for improved precision.", styles['BodyProse']))

    story.append(Paragraph("4.6 Contrastive Learning for Embeddings", styles['SectionTitle']))
    story.append(Paragraph(
        "Modern embedding models are trained using contrastive learning objectives that "
        "explicitly teach the model to distinguish similar pairs from dissimilar pairs. The "
        "InfoNCE loss (van den Oord et al., 2018) is the foundation: given a query q, a "
        "positive example p (semantically similar to q), and N negative examples n_1,...,n_N, "
        "the loss pushes q closer to p while pushing it away from all negatives.", styles['BodyProse']))
    story.append(Paragraph(
        "In-batch negatives are a key efficiency technique: within a batch of B (query, positive) "
        "pairs, each positive for one query serves as a negative for all other queries. This "
        "provides B-1 negatives for free without additional computation. Hard negative mining "
        "selects negatives that are similar to the query but not relevant, forcing the model to "
        "learn fine-grained distinctions. Models like E5 (Wang et al., 2022) and BGE (Xiao et "
        "al., 2023) achieve state-of-the-art performance by carefully curating large-scale "
        "contrastive training datasets from diverse sources.", styles['BodyProse']))
    story.append(PageBreak())


def build_chapter5(story, styles):
    story.append(Paragraph("Chapter 5: What Is a Language Model?", styles['ChapterTitle']))
    story.append(Paragraph("5.1 Probability Distributions Over Sequences", styles['SectionTitle']))
    story.append(Paragraph(
        "A language model is a probability distribution over sequences of tokens. Given a "
        "sequence of tokens (w_1, w_2, ..., w_n), a language model assigns a probability "
        "P(w_1, w_2, ..., w_n) representing how likely that sequence is to occur in natural "
        "language. Using the chain rule of probability, this joint distribution decomposes "
        "into a product of conditional probabilities:", styles['BodyProse']))
    story.append(Paragraph(
        "P(w_1, w_2, ..., w_n) = P(w_1) * P(w_2|w_1) * P(w_3|w_1,w_2) * ... * P(w_n|w_1,...,w_{n-1})",
        styles['MathBlock']))
    story.append(Paragraph(
        "Each factor P(w_t|w_1,...,w_{t-1}) represents the probability of the next token given "
        "all preceding tokens. A language model that accurately estimates these conditional "
        "probabilities has implicitly learned syntax (to predict grammatically valid "
        "continuations), semantics (to predict topically coherent continuations), and world "
        "knowledge (to predict factually consistent continuations).", styles['BodyProse']))
    story.append(Paragraph(
        "The practical significance of language models extends far beyond computing sequence "
        "probabilities. By repeatedly sampling from P(w_t|w_1,...,w_{t-1}), we generate "
        "new text one token at a time. This autoregressive generation process is the foundation "
        "of modern text generation systems. The quality of generated text depends directly on "
        "the quality of the learned probability estimates.", styles['BodyProse']))

    story.append(Paragraph("5.2 N-gram Language Models", styles['SectionTitle']))
    story.append(Paragraph(
        "The earliest practical language models were n-gram models, which apply the Markov "
        "assumption: the probability of a word depends only on the preceding (n-1) words. "
        "A bigram model (n=2) estimates P(w_t|w_{t-1}), a trigram model (n=3) estimates "
        "P(w_t|w_{t-2}, w_{t-1}). These probabilities are estimated by counting occurrences "
        "in a training corpus: P(w_t|w_{t-1}) = count(w_{t-1}, w_t) / count(w_{t-1}).", styles['BodyProse']))
    story.append(Paragraph(
        "N-gram models are simple, fast, and interpretable, but they suffer from fundamental "
        "limitations. The Markov assumption means they cannot capture long-range dependencies: "
        "in 'The cat that the dog chased ran away', a trigram model cannot connect 'cat' with "
        "'ran'. Additionally, n-gram models suffer from data sparsity: as n increases, most "
        "possible n-grams never appear in the training corpus, requiring smoothing techniques "
        "(Kneser-Ney, Good-Turing) to assign non-zero probabilities to unseen sequences.", styles['BodyProse']))
    story.append(Paragraph(
        "Despite these limitations, n-gram models were the dominant approach in speech "
        "recognition and machine translation for decades (roughly 1980-2010). They remain "
        "useful as baselines. The perplexity metric, commonly used to evaluate language models, "
        "was originally developed for n-gram models: perplexity = 2^H(P,Q) where H is the "
        "cross-entropy between the true distribution P and the model Q.", styles['BodyProse']))

    story.append(Paragraph("5.3 Neural Language Models", styles['SectionTitle']))
    story.append(Paragraph(
        "Neural language models, pioneered by Yoshua Bengio and colleagues in their seminal "
        "2003 paper 'A Neural Probabilistic Language Model' (JMLR), address the sparsity "
        "problem by learning continuous representations of words. Instead of treating each word "
        "as a discrete symbol, the model maps each word to a dense vector and learns to predict "
        "the next word as a smooth function of the preceding word vectors. Similar words "
        "(with similar embeddings) produce similar predictions, enabling generalization to "
        "unseen word combinations.", styles['BodyProse']))
    story.append(Paragraph(
        "Bengio's model was a feedforward network: concatenate the embeddings of the preceding "
        "n words, pass through a hidden layer with tanh activation, and produce a probability "
        "distribution over the vocabulary via softmax. Despite its simplicity, this architecture "
        "outperformed n-gram models with far less data. The model simultaneously learns the word "
        "embeddings and the prediction function, allowing the embedding space to organize itself "
        "for the prediction task.", styles['BodyProse']))
    story.append(Paragraph(
        "Subsequent neural language models replaced feedforward architectures with recurrent "
        "neural networks (Mikolov et al., 2010), which maintain a hidden state accumulating "
        "information from all preceding tokens. LSTM (Hochreiter and Schmidhuber, 1997) and "
        "GRU (Cho et al., 2014) variants addressed the vanishing gradient problem. These "
        "RNN-based language models dominated from 2013 to 2017 before being superseded by "
        "the Transformer.", styles['BodyProse']))

    story.append(Paragraph("5.4 Autoregressive Generation", styles['SectionTitle']))
    story.append(Paragraph(
        "Autoregressive generation produces text one token at a time by repeatedly sampling "
        "from P(w_t|w_1,...,w_{t-1}). Starting from a prompt, the model computes the probability "
        "of every possible next token, selects one, appends it to the sequence, and repeats "
        "until a stop condition is met (maximum length, end-of-sequence token).", styles['BodyProse']))
    story.append(Paragraph(
        "The sampling strategy significantly affects quality. Greedy decoding (always selecting "
        "the highest-probability token) produces repetitive text. Pure random sampling produces "
        "incoherent text. Temperature scaling divides logits by T before softmax: T < 1 "
        "sharpens the distribution (more deterministic), T > 1 flattens it (more random). "
        "Top-k sampling restricts to the k highest-probability tokens. Nucleus sampling (top-p) "
        "samples from the smallest token set whose cumulative probability exceeds threshold p, "
        "adapting dynamically to the model's confidence at each step.", styles['BodyProse']))

    story.append(Paragraph("5.5 Evaluating Language Models", styles['SectionTitle']))
    story.append(Paragraph(
        "The standard metric for evaluating language models is perplexity, defined as the "
        "exponentiation of the average cross-entropy loss: PPL = exp(-1/N * sum log P(w_t|context)). "
        "Intuitively, perplexity represents the effective number of equally-likely tokens the "
        "model considers at each position. A perplexity of 20 means the model is, on average, "
        "as uncertain as if it were choosing uniformly among 20 candidates at each step. "
        "Lower perplexity indicates a better model.", styles['BodyProse']))
    story.append(Paragraph(
        "However, perplexity has limitations as an evaluation metric. It measures how well the "
        "model predicts held-out text, but does not directly measure the quality of generated "
        "text or the model's ability to follow instructions. A model might have excellent "
        "perplexity on news articles but generate incoherent creative writing. For this reason, "
        "modern LLM evaluation increasingly relies on benchmark suites (MMLU, HellaSwag, "
        "ARC, TruthfulQA) that test specific capabilities like reasoning, knowledge recall, "
        "and truthfulness, as well as human evaluations for open-ended generation quality.", styles['BodyProse']))

    story.append(Paragraph("5.6 The Transition from Statistical to Neural Models", styles['SectionTitle']))
    story.append(Paragraph(
        "The transition from n-gram to neural language models occurred gradually from 2010 to "
        "2015. Mikolov et al. (2010, 2011) showed that simple RNN language models could outperform "
        "large n-gram models on speech recognition. Jozefowicz et al. (2016) at Google demonstrated "
        "that large LSTM language models achieved state-of-the-art perplexity on the One Billion "
        "Word Benchmark, outperforming the best smoothed n-gram models by a substantial margin. "
        "By 2017, neural language models had completely displaced n-gram models in all major "
        "NLP applications.", styles['BodyProse']))
    story.append(Paragraph(
        "The advantages of neural language models are threefold. First, they generalize better "
        "because similar words (those with similar embeddings) make similar predictions, even for "
        "n-grams never seen during training. Second, they capture longer-range dependencies through "
        "recurrent or attention-based architectures. Third, they can be pre-trained on unlabeled "
        "text and transferred to downstream tasks, amortizing the cost of learning linguistic "
        "structure across many applications.", styles['BodyProse']))
    story.append(PageBreak())


def build_chapter6(story, styles):
    story.append(Paragraph("Chapter 6: The Transformer Architecture", styles['ChapterTitle']))
    story.append(Paragraph("6.1 Motivation: Beyond Recurrence", styles['SectionTitle']))
    story.append(Paragraph(
        "The Transformer was introduced in 'Attention Is All You Need' by Ashish Vaswani, "
        "Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz "
        "Kaiser, and Illia Polosukhin, published at NeurIPS 2017. The central argument is that "
        "the attention mechanism alone, without any recurrence or convolution, is sufficient for "
        "modeling sequence-to-sequence tasks\u2014and is superior to RNN-based architectures in "
        "both quality and training efficiency.", styles['BodyProse']))
    story.append(Paragraph(
        "The fundamental limitation of RNNs is their sequential nature: to compute the "
        "representation at position t, the model must first compute all positions 1 through "
        "t-1. This prevents parallelization during training. For long sequences, information "
        "from early tokens must pass through many processing steps, leading to vanishing "
        "gradients despite LSTM/GRU gating mechanisms.", styles['BodyProse']))
    story.append(Paragraph(
        "The Transformer eliminates this bottleneck entirely. Through self-attention, every "
        "position directly attends to every other position in a single computational step, "
        "regardless of distance. The path length between any two positions is O(1) rather than "
        "O(n), dramatically improving gradient flow. Furthermore, the self-attention computation "
        "at all positions can be performed in parallel as a single matrix multiplication.", styles['BodyProse']))

    story.append(Paragraph("6.2 Input Embedding and Positional Encoding", styles['SectionTitle']))
    story.append(Paragraph(
        "Input tokens are mapped to d_model-dimensional vectors (d_model = 512 in the base "
        "model). Since self-attention treats input as a set with no inherent order, positional "
        "information must be explicitly injected. The original Transformer uses sinusoidal "
        "positional encodings:", styles['BodyProse']))
    story.append(Paragraph(
        "PE(pos, 2i) = sin(pos / 10000^(2i/d_model))\n"
        "PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))",
        styles['MathBlock']))
    story.append(Paragraph(
        "Each dimension corresponds to a sinusoid with a different wavelength, forming a "
        "geometric progression from 2*pi to 10000*2*pi. This allows the model to learn "
        "relative positions through linear projections, since PE(pos+k) can be expressed "
        "as a linear function of PE(pos) for any fixed offset k. Later models (BERT, GPT) "
        "replaced sinusoidal encodings with learned positional embeddings.", styles['BodyProse']))

    story.append(Paragraph("6.3 Self-Attention Mechanism", styles['SectionTitle']))
    story.append(Paragraph(
        "Self-attention is the core operation. For each position, it computes a weighted sum "
        "over all positions, where weights are determined by compatibility. The input X "
        "(shape [n x d_model]) is projected into Queries Q = X*W_Q, Keys K = X*W_K, and "
        "Values V = X*W_V through learned weight matrices:", styles['BodyProse']))
    story.append(Paragraph(
        "Attention(Q, K, V) = softmax(Q * K^T / sqrt(d_k)) * V",
        styles['MathBlock']))
    story.append(Paragraph(
        "The Query represents what a position is looking for, the Key represents what it "
        "offers, and the Value is the information to be aggregated. The scaling factor "
        "1/sqrt(d_k) prevents dot products from growing too large (which would push softmax "
        "into regions with extremely small gradients). After softmax, attention weights sum "
        "to 1 for each query position, forming a probability distribution over key positions.", styles['BodyProse']))
    story.append(Paragraph(
        "Intuitively, self-attention allows each word to 'look at' every other word and decide "
        "how much information to incorporate. In 'The animal didn't cross the street because "
        "it was too tired', the word 'it' must attend strongly to 'animal' to resolve the "
        "coreference. Self-attention learns such patterns directly from data.", styles['BodyProse']))

    story.append(Paragraph("6.4 Multi-Head Attention", styles['SectionTitle']))
    story.append(Paragraph(
        "Rather than one attention function with d_model-dimensional keys, values, and queries, "
        "the Transformer uses h parallel attention heads, each on a lower-dimensional projection. "
        "In the base model, h = 8 heads with d_k = d_v = d_model/h = 64 dimensions each:", styles['BodyProse']))
    story.append(Paragraph(
        "MultiHead(Q, K, V) = Concat(head_1, ..., head_h) * W_O\n"
        "where head_i = Attention(Q*W_Q_i, K*W_K_i, V*W_V_i)",
        styles['MathBlock']))
    story.append(Paragraph(
        "Multiple heads allow the model to jointly attend to information from different "
        "representation subspaces. One head might learn syntactic dependencies, another "
        "semantic relationships, and another positional patterns. This factorized attention "
        "is more expressive than single-head attention with the same total dimensionality.", styles['BodyProse']))

    story.append(Paragraph("6.5 Feed-Forward Network and Residual Connections", styles['SectionTitle']))
    story.append(Paragraph(
        "Each Transformer layer also contains a position-wise feed-forward network (FFN) "
        "applied independently to each position:", styles['BodyProse']))
    story.append(Paragraph(
        "FFN(x) = max(0, x*W_1 + b_1) * W_2 + b_2",
        styles['MathBlock']))
    story.append(Paragraph(
        "The FFN has two linear transformations with a ReLU activation between them. The "
        "inner dimension d_ff = 2048 (four times d_model = 512) creates a bottleneck. Research "
        "suggests FFN layers serve as key-value memories: the first layer encodes patterns to "
        "match (keys), and the second encodes information to retrieve (values).", styles['BodyProse']))
    story.append(Paragraph(
        "Both sublayers use residual connections (He et al., 2016) followed by layer "
        "normalization (Ba et al., 2016): LayerNorm(x + Sublayer(x)). Residual connections "
        "allow gradients to flow directly through the network without degradation. Layer "
        "normalization stabilizes training by normalizing activations to zero mean and unit "
        "variance at each layer.", styles['BodyProse']))

    story.append(Paragraph("6.6 Encoder-Decoder Architecture", styles['SectionTitle']))
    story.append(Paragraph(
        "The original Transformer uses an encoder-decoder architecture. The encoder has N = 6 "
        "identical layers, each with self-attention and FFN sublayers. The decoder also has "
        "N = 6 layers with masked self-attention (preventing attention to future tokens), "
        "cross-attention (attending to encoder outputs), and FFN sublayers.", styles['BodyProse']))
    story.append(Paragraph(
        "The base model: d_model=512, d_ff=2048, h=8 heads, N=6 layers in both encoder and "
        "decoder, totaling approximately 65 million parameters. The large model scales to "
        "d_model=1024, d_ff=4096, h=16 heads, with approximately 213 million parameters. "
        "Despite being introduced for machine translation, the Transformer became the "
        "foundation for virtually all subsequent advances in NLP, computer vision, speech "
        "processing, and protein structure prediction.", styles['BodyProse']))

    story.append(Paragraph("6.7 Computational Complexity and Efficiency", styles['SectionTitle']))
    story.append(Paragraph(
        "The self-attention mechanism has O(n^2 * d) time and O(n^2) space complexity, where n "
        "is the sequence length and d is the model dimension. This quadratic scaling with sequence "
        "length is the primary bottleneck of the Transformer architecture. For a sequence of "
        "4,096 tokens, self-attention produces a 4096 x 4096 attention matrix (about 67 million "
        "entries per head, per layer). This motivates research into efficient attention variants.", styles['BodyProse']))
    story.append(Paragraph(
        "Several approaches address this quadratic complexity. Sparse attention (Child et al., "
        "2019) attends only to a subset of positions using fixed or learned sparsity patterns. "
        "Linear attention (Katharopoulos et al., 2020) replaces softmax with a kernel function "
        "that allows reformulation as a linear recurrence. Flash Attention (Dao et al., 2022) "
        "does not change the mathematical computation but achieves 2-4x speedups by optimizing "
        "memory access patterns to exploit GPU memory hierarchy (reducing reads/writes between "
        "HBM and SRAM). Flash Attention has become the standard implementation for training "
        "modern LLMs.", styles['BodyProse']))

    story.append(Paragraph("6.8 Variants: Encoder-Only, Decoder-Only, Encoder-Decoder", styles['SectionTitle']))
    story.append(Paragraph(
        "The Transformer architecture has spawned three major variants. Encoder-only models "
        "(BERT, RoBERTa, ELECTRA) use bidirectional self-attention and are trained with masked "
        "language modeling. They excel at classification, token labeling, and extracting "
        "representations, but cannot generate text autoregressively. Decoder-only models "
        "(GPT, LLaMA, PaLM) use causal (masked) self-attention and are trained with next-token "
        "prediction. They excel at text generation and have become the dominant architecture for "
        "general-purpose LLMs.", styles['BodyProse']))
    story.append(Paragraph(
        "Encoder-decoder models (T5, BART, mBART) use the full original architecture with "
        "bidirectional encoding and causal decoding with cross-attention. They excel at "
        "sequence-to-sequence tasks like translation, summarization, and question answering. "
        "The choice between architectures depends on the application: encoder-only for "
        "understanding tasks, decoder-only for generation, encoder-decoder for transduction. "
        "However, the trend since 2020 has been toward decoder-only models, which can handle "
        "all these tasks through appropriate prompting and fine-tuning.", styles['BodyProse']))
    story.append(PageBreak())


def build_chapter7(story, styles):
    story.append(Paragraph("Chapter 7: From Transformer to GPT", styles['ChapterTitle']))
    story.append(Paragraph("7.1 GPT-1: Generative Pre-Training (Radford et al., 2018)", styles['SectionTitle']))
    story.append(Paragraph(
        "GPT-1, introduced by Alec Radford, Karthik Narasimhan, Tim Salimans, and Ilya "
        "Sutskever at OpenAI in 'Improving Language Understanding by Generative Pre-Training' "
        "(2018), demonstrated that a decoder-only Transformer pre-trained on unlabeled text "
        "could be fine-tuned to achieve strong performance on diverse NLP tasks. This "
        "established the pre-train then fine-tune paradigm.", styles['BodyProse']))
    story.append(Paragraph(
        "GPT-1 uses a 12-layer decoder-only Transformer with 768-dimensional hidden states, "
        "12 attention heads, and 117 million parameters. It was pre-trained on BooksCorpus "
        "(approximately 800 million words from 7,000 unpublished books) using next-token "
        "prediction. The key insight was that unsupervised pre-training provides a powerful "
        "initialization for supervised fine-tuning on downstream tasks.", styles['BodyProse']))
    story.append(Paragraph(
        "During fine-tuning, task-specific input transformations convert each task into a "
        "sequence format. For text classification, the input is followed by a delimiter and "
        "a classification layer. For entailment, premise and hypothesis are concatenated. "
        "This unified approach allowed a single pre-trained model to be adapted to many "
        "tasks with minimal architectural modifications.", styles['BodyProse']))

    story.append(Paragraph("7.2 GPT-2: Zero-Shot Transfer (Radford et al., 2019)", styles['SectionTitle']))
    story.append(Paragraph(
        "GPT-2, described in 'Language Models are Unsupervised Multitask Learners' (2019), "
        "scaled up by 10x in both model size and data. The largest GPT-2 model has 1.5 billion "
        "parameters (48 layers, 1600-dimensional hidden states, 25 attention heads) trained on "
        "WebText, approximately 40GB of text from Reddit links with at least 3 karma.", styles['BodyProse']))
    story.append(Paragraph(
        "GPT-2's key contribution was demonstrating zero-shot task performance: the model "
        "could perform tasks it was never trained for by conditioning on appropriate prompts. "
        "For example, it could perform reading comprehension by conditioning on a document "
        "followed by a question, or translation by providing 'translate English to French:' "
        "followed by an English sentence. While below supervised systems, this suggested that "
        "larger language models might develop general task-solving abilities.", styles['BodyProse']))
    story.append(Paragraph(
        "OpenAI initially declined to release the full model due to misuse concerns around "
        "disinformation generation, releasing it in stages over several months. This decision "
        "sparked important discussions about responsible AI development and the dual-use nature "
        "of powerful language models. The model was fully released in November 2019.", styles['BodyProse']))

    story.append(Paragraph("7.3 GPT-3: In-Context Learning (Brown et al., 2020)", styles['SectionTitle']))
    story.append(Paragraph(
        "GPT-3, described in 'Language Models are Few-Shot Learners' (Brown et al., 2020), "
        "scales to 175 billion parameters (96 layers, 12,288-dimensional hidden states, 96 "
        "attention heads). It was trained on a filtered Common Crawl (410 billion tokens), "
        "supplemented with WebText, Books, and English Wikipedia, totaling approximately 300 "
        "billion tokens.", styles['BodyProse']))
    story.append(Paragraph(
        "GPT-3's defining capability is in-context learning (few-shot learning): providing "
        "a few examples of a task in the prompt causes the model to perform the task on new "
        "inputs without any gradient updates. For example, providing three English-French "
        "translation pairs followed by a new English sentence causes GPT-3 to produce the "
        "French translation. The model performs the task purely by pattern-matching on the "
        "examples provided in context.", styles['BodyProse']))
    story.append(Paragraph(
        "Key findings: (1) performance improves log-linearly with model size; (2) larger "
        "models are more sample-efficient in few-shot settings; (3) few-shot GPT-3 matches "
        "or exceeds fine-tuned BERT on several benchmarks despite never updating its weights. "
        "GPT-3 also demonstrated strong performance on tasks requiring reasoning, arithmetic, "
        "and world knowledge.", styles['BodyProse']))

    story.append(Paragraph("7.4 Scaling Laws (Kaplan et al., 2020)", styles['SectionTitle']))
    story.append(Paragraph(
        "'Scaling Laws for Neural Language Models' by Jared Kaplan, Sam McCandlish, Tom "
        "Henighan, and colleagues at OpenAI (2020) established empirical power-law "
        "relationships between model performance and three key factors: model size (N), "
        "dataset size (D), and compute budget (C):", styles['BodyProse']))
    story.append(Paragraph(
        "L(N) ~ N^(-0.076)   (loss as a function of parameters)\n"
        "L(D) ~ D^(-0.095)   (loss as a function of dataset tokens)\n"
        "L(C) ~ C^(-0.050)   (loss as a function of compute)",
        styles['MathBlock']))
    story.append(Paragraph(
        "These predict that performance improvements are smooth and predictable: doubling "
        "model size reduces loss by a fixed amount on a log scale. Model shape (depth vs. "
        "width) has relatively little effect compared to total parameter count. Additionally, "
        "larger models are more sample-efficient, achieving the same loss with fewer training "
        "tokens.", styles['BodyProse']))

    story.append(Paragraph("7.5 Chinchilla: Compute-Optimal Training (Hoffmann et al., 2022)", styles['SectionTitle']))
    story.append(Paragraph(
        "'Training Compute-Optimal Large Language Models' by Jordan Hoffmann et al. at "
        "DeepMind (2022) revisited optimal compute allocation. While Kaplan et al. suggested "
        "allocating most compute to larger models, Chinchilla found the optimal ratio is "
        "approximately 20 training tokens per model parameter.", styles['BodyProse']))
    story.append(Paragraph(
        "This implied many existing models were significantly undertrained. Chinchilla, a 70B "
        "parameter model trained on 1.4 trillion tokens, outperformed the 280B parameter Gopher "
        "on virtually every benchmark. The implication: rather than always building bigger "
        "models, train smaller models on more data. This influenced LLaMA (Touvron et al., "
        "2023), which trained a 65B model on 1.4 trillion tokens.", styles['BodyProse']))

    story.append(Paragraph("7.6 Open-Source LLMs and Democratization", styles['SectionTitle']))
    story.append(Paragraph(
        "LLaMA (Large Language Model Meta AI), released by Touvron et al. at Meta in February "
        "2023, marked a turning point for open-source LLMs. The LLaMA family (7B, 13B, 33B, "
        "65B parameters) was trained following the Chinchilla-optimal recipe: the 65B model was "
        "trained on 1.4 trillion tokens from publicly available data sources. LLaMA-13B "
        "outperformed GPT-3 (175B) on most benchmarks, demonstrating that smaller, well-trained "
        "models can match or exceed much larger ones.", styles['BodyProse']))
    story.append(Paragraph(
        "The release of LLaMA weights (initially restricted to researchers) catalyzed an "
        "explosion of open-source development. Stanford Alpaca demonstrated that fine-tuning "
        "LLaMA-7B on 52K instruction-following examples generated by GPT-3.5 produced a "
        "capable instruction-following model at minimal cost. Vicuna (LMSYS) fine-tuned on "
        "ShareGPT conversations achieved 90% of ChatGPT quality according to GPT-4 evaluations. "
        "These developments showed that alignment and instruction-following capabilities could "
        "be added cheaply to any base model through fine-tuning.", styles['BodyProse']))
    story.append(Paragraph(
        "Subsequent open models\u2014LLaMA 2 (Meta, July 2023), Mistral 7B (Mistral AI, "
        "September 2023), Mixtral 8x7B (a mixture-of-experts model), and LLaMA 3 (Meta, "
        "April 2024)\u2014have progressively closed the gap with proprietary models. LLaMA 3 "
        "70B approaches GPT-4 quality on many benchmarks. This trend toward powerful open models "
        "has democratized access to LLM capabilities, enabling researchers, startups, and "
        "organizations to deploy and customize models without depending on API providers.", styles['BodyProse']))
    story.append(PageBreak())


def build_chapter8(story, styles):
    story.append(Paragraph("Chapter 8: Training an LLM from Scratch", styles['ChapterTitle']))
    story.append(Paragraph("8.1 Data Collection and Preprocessing", styles['SectionTitle']))
    story.append(Paragraph(
        "Training a large language model begins with assembling a massive text corpus. Modern "
        "LLMs are trained on hundreds of billions to trillions of tokens from diverse sources. "
        "Common Crawl provides petabytes of raw HTML data. However, raw web data contains "
        "boilerplate, duplicate content, low-quality text, and potentially harmful material "
        "that must be filtered.", styles['BodyProse']))
    story.append(Paragraph(
        "The Pile (Gao et al., 2020) is an influential 800GB English text dataset combining "
        "22 high-quality sources including academic papers (PubMed, ArXiv), books, code "
        "(GitHub), web content, and specialized sources (USPTO patents, Ubuntu IRC). This "
        "diversity is intentional: models trained on diverse data develop broader capabilities.", styles['BodyProse']))
    story.append(Paragraph(
        "Preprocessing involves deduplication (MinHash locality-sensitive hashing, reducing "
        "size by 30-50%), quality filtering (document length, alphabetic proportion, "
        "perplexity under a reference model), PII scrubbing (removing phone numbers, emails), "
        "and toxic content filtering using classifiers.", styles['BodyProse']))

    story.append(Paragraph("8.2 Tokenization", styles['SectionTitle']))
    story.append(Paragraph(
        "Text must be converted into discrete tokens before being fed to a model. Modern LLMs "
        "use subword tokenization\u2014units smaller than words but larger than characters\u2014"
        "achieving a balance between vocabulary size and sequence length.", styles['BodyProse']))
    story.append(Paragraph(
        "Byte Pair Encoding (BPE), originally a compression algorithm (Gage, 1994), was adapted "
        "for NLP by Sennrich et al. (2016). BPE starts with a character-level vocabulary and "
        "iteratively merges the most frequent adjacent pair of tokens. For example, ('t', 'h') "
        "becomes 'th', then ('th', 'e') becomes 'the'. This continues until the desired "
        "vocabulary size (typically 32,000 to 100,000 tokens) is reached.", styles['BodyProse']))
    story.append(Paragraph(
        "SentencePiece (Kudo and Richardson, 2018) is a language-independent tokenization "
        "library implementing BPE and unigram tokenization. Unlike traditional tokenizers "
        "requiring whitespace-split input, SentencePiece operates directly on raw Unicode, "
        "treating whitespace as a regular character. This makes it suitable for languages "
        "without clear word boundaries (Chinese, Japanese, Thai).", styles['BodyProse']))

    story.append(Paragraph("8.3 Training Objective and Architecture Decisions", styles['SectionTitle']))
    story.append(Paragraph(
        "The standard training objective for decoder-only LLMs is next-token prediction with "
        "cross-entropy loss:", styles['BodyProse']))
    story.append(Paragraph(
        "L = -sum_{t=1}^{T} log P(x_t | x_1, ..., x_{t-1})",
        styles['MathBlock']))
    story.append(Paragraph(
        "Architecture decisions include: number of layers, hidden dimension, attention heads, "
        "feed-forward dimension (typically 4x hidden dim), context length, and vocabulary size. "
        "Current trends favor deeper models: GPT-3 uses 96 layers with d_model=12,288; "
        "LLaMA 65B uses 80 layers with d_model=8,192. Context lengths have grown from 512 "
        "(BERT) to 2048 (GPT-2) to 128,000+ tokens in recent models.", styles['BodyProse']))
    story.append(Paragraph(
        "Modern refinements include: RMSNorm (Zhang and Sennrich, 2019) replacing LayerNorm; "
        "Rotary Position Embeddings (RoPE, Su et al., 2021) for better length generalization; "
        "SwiGLU activation (Shazeer, 2020) replacing ReLU; and Grouped Query Attention "
        "(GQA, Ainslie et al., 2023) reducing key-value cache size for faster inference.", styles['BodyProse']))

    story.append(Paragraph("8.4 Optimization and Hardware", styles['SectionTitle']))
    story.append(Paragraph(
        "The standard optimizer is AdamW (Loshchilov and Hutter, 2019), combining adaptive "
        "learning rates with decoupled weight decay. Typical hyperparameters: learning rate "
        "1e-4 to 3e-4, beta_1=0.9, beta_2=0.95, weight decay 0.1, gradient clipping at 1.0. "
        "The schedule uses linear warmup over 1,000-2,000 steps followed by cosine decay to "
        "10% of peak learning rate.", styles['BodyProse']))
    story.append(Paragraph(
        "Training GPT-3 required approximately 3.14 x 10^23 FLOPs, equivalent to thousands "
        "of GPU-days on NVIDIA A100 accelerators. This necessitates distributed training: "
        "data parallelism (splitting batches), tensor parallelism (splitting operations), "
        "and pipeline parallelism (splitting layers). Frameworks like Megatron-LM (Shoeybi "
        "et al., 2019), DeepSpeed (Rasley et al., 2020), and FSDP enable this.", styles['BodyProse']))

    story.append(Paragraph("8.5 RLHF: Aligning Models with Human Preferences", styles['SectionTitle']))
    story.append(Paragraph(
        "Reinforcement Learning from Human Feedback (RLHF), as described in 'Training language "
        "models to follow instructions with human feedback' (Ouyang et al., 2022)\u2014the "
        "InstructGPT paper\u2014transforms a pre-trained language model into an assistant that "
        "follows instructions and aligns with human preferences.", styles['BodyProse']))
    story.append(Paragraph(
        "The RLHF pipeline has three stages. Stage 1: Supervised Fine-Tuning (SFT)\u2014the "
        "pre-trained model is fine-tuned on human-written demonstrations. Stage 2: Reward "
        "Model Training\u2014a separate model learns to predict human preferences by training "
        "on ranked model outputs. Stage 3: RL Optimization\u2014the SFT model is further "
        "trained using Proximal Policy Optimization (PPO, Schulman et al., 2017) to maximize "
        "reward model scores while staying close to the SFT model via KL divergence penalty.", styles['BodyProse']))
    story.append(Paragraph(
        "InstructGPT showed that a 1.3B parameter RLHF model was preferred by human evaluators "
        "over the 175B parameter GPT-3, demonstrating that alignment can be more impactful "
        "than scale alone.", styles['BodyProse']))

    story.append(Paragraph("8.6 The Complete Training Pipeline", styles['SectionTitle']))
    story.append(Paragraph(
        "The modern LLM training pipeline: Phase 1: Pre-training\u2014train a Transformer on "
        "trillions of tokens using next-token prediction. This is the most expensive phase, "
        "producing a base model good at text completion but not at following instructions. "
        "Phase 2: Supervised Fine-Tuning (SFT)\u2014fine-tune on thousands to millions of "
        "(instruction, response) pairs.", styles['BodyProse']))
    story.append(Paragraph(
        "Phase 3: Alignment\u2014apply RLHF, DPO (Direct Preference Optimization, Rafailov "
        "et al., 2023), or related techniques. Pre-training provides broad knowledge, SFT "
        "teaches instruction-following behavior, and alignment refines outputs to match human "
        "values. The resulting model is what users interact with as a conversational AI.", styles['BodyProse']))

    story.append(Paragraph("8.7 Inference Optimization", styles['SectionTitle']))
    story.append(Paragraph(
        "Deploying LLMs efficiently requires significant inference optimization. The key "
        "bottleneck during autoregressive generation is the KV cache: at each generation step, "
        "the model must store the key and value vectors from all previous tokens across all "
        "layers and heads. For a 70B parameter model generating a 4096-token sequence, the "
        "KV cache alone can consume 40+ GB of GPU memory.", styles['BodyProse']))
    story.append(Paragraph(
        "Quantization reduces the memory footprint by representing model weights in lower "
        "precision. Standard training uses 16-bit floating point (FP16/BF16), but inference "
        "can often use 8-bit integers (INT8) or even 4-bit integers (INT4) with minimal quality "
        "loss. GPTQ (Frantar et al., 2022) and AWQ (Lin et al., 2023) are post-training "
        "quantization methods that calibrate on a small dataset to minimize quantization error. "
        "A 70B model at 4-bit precision fits on a single 48GB GPU (A6000 or A100).", styles['BodyProse']))
    story.append(Paragraph(
        "Speculative decoding (Leviathan et al., 2023; Chen et al., 2023) uses a small draft "
        "model to propose multiple tokens quickly, then verifies them in parallel with the full "
        "model. Since verification can process multiple tokens simultaneously (unlike generation), "
        "this achieves 2-3x speedup without any quality loss. Other optimizations include "
        "continuous batching (processing multiple requests simultaneously, filling in new "
        "requests as others complete), paged attention (PagedAttention, Kwon et al., 2023) for "
        "efficient KV cache memory management, and tensor parallelism across multiple GPUs.", styles['BodyProse']))

    story.append(Paragraph("8.8 Emergent Capabilities and Limitations", styles['SectionTitle']))
    story.append(Paragraph(
        "As language models scale, they exhibit emergent capabilities\u2014abilities that appear "
        "suddenly at certain model sizes rather than improving gradually. Wei et al. (2022) "
        "documented several emergent abilities including multi-step arithmetic, multi-step "
        "reasoning, and understanding of novel word definitions from context. These capabilities "
        "are absent in smaller models and appear abruptly above certain parameter thresholds.", styles['BodyProse']))
    story.append(Paragraph(
        "Despite their remarkable capabilities, LLMs have well-documented limitations. "
        "Hallucination\u2014generating plausible but factually incorrect statements\u2014remains "
        "a persistent problem, especially for obscure facts or when the model is asked about "
        "topics beyond its training data. LLMs struggle with precise arithmetic, especially "
        "involving large numbers. They have no mechanism for updating their knowledge after "
        "training (the knowledge cutoff problem). They can exhibit biases present in their "
        "training data. And they lack true understanding\u2014they pattern-match on statistical "
        "regularities rather than building causal models of the world.", styles['BodyProse']))
    story.append(Paragraph(
        "Active research addresses these limitations through various approaches: retrieval-"
        "augmented generation (RAG) for grounding in factual sources, chain-of-thought prompting "
        "and reasoning frameworks for improved logical consistency, tool use for precise "
        "computation and information retrieval, and continued pre-training or knowledge editing "
        "for updating model knowledge. The trajectory of the field suggests that many current "
        "limitations are engineering challenges rather than fundamental barriers.", styles['BodyProse']))
    story.append(PageBreak())


def build_references(story, styles):
    story.append(Paragraph("References", styles['ChapterTitle']))
    refs = [
        "Bengio, Y., Ducharme, R., Vincent, P., and Jauvin, C. (2003). A Neural Probabilistic "
        "Language Model. Journal of Machine Learning Research, 3, 1137-1155.",
        "Brown, T. B., Mann, B., Ryder, N., Subbiah, M., et al. (2020). Language Models are "
        "Few-Shot Learners. NeurIPS. arXiv:2005.14165",
        "Devlin, J., Chang, M.-W., Lee, K., and Toutanova, K. (2019). BERT: Pre-training of "
        "Deep Bidirectional Transformers for Language Understanding. NAACL. arXiv:1810.04805",
        "Hoffmann, J., Borgeaud, S., Mensch, A., et al. (2022). Training Compute-Optimal "
        "Large Language Models. NeurIPS. arXiv:2203.15556",
        "Kaplan, J., McCandlish, S., Henighan, T., et al. (2020). Scaling Laws for Neural "
        "Language Models. arXiv:2001.08361",
        "Kusupati, A., Bhatt, G., Rege, A., et al. (2022). Matryoshka Representation Learning. "
        "NeurIPS. arXiv:2205.13147",
        "Mikolov, T., Chen, K., Corrado, G., and Dean, J. (2013). Efficient Estimation of Word "
        "Representations in Vector Space. ICLR Workshop. arXiv:1301.3781",
        "Mikolov, T., Sutskever, I., Chen, K., Corrado, G., and Dean, J. (2013). Distributed "
        "Representations of Words and Phrases and their Compositionality. NeurIPS. arXiv:1310.4546",
        "Muennighoff, N., Tazi, N., Magne, L., and Reimers, N. (2023). MTEB: Massive Text "
        "Embedding Benchmark. EACL. arXiv:2210.07316",
        "Ouyang, L., Wu, J., Jiang, X., et al. (2022). Training language models to follow "
        "instructions with human feedback. NeurIPS. arXiv:2203.02155",
        "Pennington, J., Socher, R., and Manning, C. D. (2014). GloVe: Global Vectors for Word "
        "Representation. EMNLP. https://nlp.stanford.edu/projects/glove/",
        "Peters, M. E., Neumann, M., Iyyer, M., et al. (2018). Deep contextualized word "
        "representations. NAACL. arXiv:1802.05365",
        "Radford, A., Narasimhan, K., Salimans, T., and Sutskever, I. (2018). Improving Language "
        "Understanding by Generative Pre-Training. OpenAI Technical Report.",
        "Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., and Sutskever, I. (2019). "
        "Language Models are Unsupervised Multitask Learners. OpenAI Technical Report.",
        "Reimers, N. and Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese "
        "BERT-Networks. EMNLP-IJCNLP. arXiv:1908.10084",
        "Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., "
        "Kaiser, L., and Polosukhin, I. (2017). Attention Is All You Need. NeurIPS. arXiv:1706.03762",
    ]
    for ref in refs:
        story.append(Paragraph(ref, styles['RefStyle']))
        story.append(Spacer(1, 4))


def generate(output_path=None):
    if output_path is None:
        output_path = OUTPUT_PATH
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = get_styles()
    story = []

    build_title_page(story, styles)
    build_chapter1(story, styles)
    build_chapter2(story, styles)
    build_chapter3(story, styles)
    build_chapter4(story, styles)
    build_chapter5(story, styles)
    build_chapter6(story, styles)
    build_chapter7(story, styles)
    build_chapter8(story, styles)
    build_references(story, styles)

    doc.build(story)
    print(f"Generated: {output_path} ({output_path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    generate()
