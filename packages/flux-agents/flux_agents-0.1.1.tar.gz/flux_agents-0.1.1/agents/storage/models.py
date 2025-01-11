from pydantic import BaseModel, Field
from functools import lru_cache
from enum import Enum
from itertools import count
from typing import List, Dict, Any, Optional, Type
from uuid import uuid4
from threading import Lock

from utils.shared.tokenizer import encode, decode

from agents.config.models import TruncationType


class IDFactory:
    """
    Factory for generating unique IDs per class.
    Maintains separate counters for different classes.
    """
    _counters: Dict[str, count] = {}
    _lock = Lock()

    @classmethod
    def next_id(cls, owner_class: Type) -> int:
        """
        Get next ID for the specified class.
        
        :param owner_class: Class requesting the ID
        :type owner_class: Type
        :return: Next available ID for that class
        :rtype: int
        """
        class_name = owner_class.__name__
        with cls._lock:
            if class_name not in cls._counters:
                cls._counters[class_name] = count(0)
            return next(cls._counters[class_name])

    @classmethod
    def reset(cls, owner_class: Optional[Type] = None) -> None:
        """
        Reset ID counter(s).
        
        :param owner_class: Optional specific class to reset counter for.
                          If None, resets all counters.
        :type owner_class: Optional[Type]
        """
        with cls._lock:
            if owner_class:
                class_name = owner_class.__name__
                cls._counters[class_name] = count(0)
            else:
                cls._counters.clear()


class Chunk(BaseModel):
    """
    Represents a chunk of content from a file.
    """
    id: int = Field(default_factory=lambda: IDFactory.next_id(Chunk))
    content: str
    path: Optional[str] = None
    parent_id: Optional[int] = None
    file_metadata: Dict[str, Any] = Field(default_factory=dict)
    score: Optional[float] = None

    def __len__(self) -> int:
        """Get token length of chunk content."""
        tokens = encode(self.content)
        return len(tokens)

    def truncate(
        self,
        max_tokens: int,
        truncation_type: TruncationType
    ) -> str:
        """
        Truncate chunk content to max tokens.
        
        :param max_tokens: Maximum number of tokens
        :param truncation_type: Type of truncation to apply
        :return: Truncated content
        """
        tokens = encode(self.content)
        if len(tokens) <= max_tokens:
            return self.content
            
        if truncation_type in [TruncationType.TOKEN_LIMIT, TruncationType.TRIM_MAX]:
            truncated_tokens = tokens[:max_tokens]
        else:  # For other types, preserve context around truncation
            # Keep some context from start and end
            context_tokens = max_tokens // 4
            middle_tokens = max_tokens - (2 * context_tokens)
            truncated_tokens = (
                tokens[:context_tokens] +
                tokens[len(tokens)//2 - middle_tokens//2:len(tokens)//2 + middle_tokens//2] +
                tokens[-context_tokens:]
            )
            
        return decode(truncated_tokens)


    def serialize(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "path": self.path,
            "score": self.score
        }
        
        
    @classmethod
    async def deserialize(cls, data: Dict[str, Any]) -> 'Chunk':
        return cls(
            id = data["id"],
            content = data["content"],
            path = data["path"],
            score = data["score"]
        )

    def __hash__(self) -> int:
        """Make Chunk hashable for caching"""
        return hash(self.id)
    
    def __eq__(self, other: object) -> bool:
        """Define equality for hashing"""
        if not isinstance(other, Chunk):
            return False
        return self.id == other.id

    @lru_cache(maxsize=1)
    def tokens(self) -> List[int]:
        """Get tokenized content"""
        return encode(self.content)


class FileType(str, Enum):
    """
    Standardized file types mapped from extensions.
    
    :cvar PYTHON: Python source and bytecode files (.py, .pyx, .pyi, .pyc)
    :cvar JAVA: Java source and class files (.java, .class, .jar)
    :cvar CPP: C++ source and header files (.cpp, .cc, .cxx, .hpp, .h)
    :cvar CSHARP: C# source files (.cs, .cshtml)
    :cvar GO: Go source files (.go)
    :cvar RUST: Rust source files (.rs)
    :cvar PHP: PHP source files (.php, .phtml)
    :cvar RUBY: Ruby source files (.rb, .erb)
    :cvar SWIFT: Swift source files (.swift)
    :cvar KOTLIN: Kotlin source files (.kt, .kts)
    :cvar SCALA: Scala source files (.scala)
    :cvar R: R source and markdown files (.r, .rmd)
    :cvar SHELL: Shell script files (.sh, .bash, .zsh)
    :cvar SQL: SQL query files (.sql, .psql, .mysql)
    :cvar HTML: HTML files (.html, .htm, .xhtml)
    :cvar CSS: CSS and preprocessor files (.css, .scss, .sass, .less)
    :cvar XML: XML and XSLT files (.xml, .xsl, .xslt)
    :cvar JSON: JSON files (.json, .jsonl)
    :cvar YAML: YAML files (.yml, .yaml)
    :cvar MARKDOWN: Markdown files (.md, .markdown)
    :cvar TEXT: Plain text files (.txt, .text)
    :cvar PDF: PDF documents (.pdf)
    :cvar DOC: Word documents (.doc, .docx)
    :cvar EXCEL: Excel spreadsheets (.xls, .xlsx, .csv)
    :cvar PPT: PowerPoint presentations (.ppt, .pptx)
    :cvar RTF: Rich text format files (.rtf)
    :cvar TEX: LaTeX files (.tex, .latex)
    :cvar IMAGE: Image files (.jpg, .jpeg, .png, .gif, .bmp, .svg, .webp)
    :cvar AUDIO: Audio files (.mp3, .wav, .ogg, .m4a, .flac)
    :cvar VIDEO: Video files (.mp4, .avi, .mov, .wmv, .flv, .webm)
    :cvar ARCHIVE: Archive files (.zip, .tar, .gz, .7z, .rar)
    :cvar CSV: CSV data files (.csv)
    :cvar PARQUET: Parquet data files (.parquet)
    :cvar HDF5: HDF5 data files (.h5, .hdf5)
    :cvar PICKLE: Python pickle files (.pkl, .pickle)
    :cvar CONFIG: Configuration files (.conf, .cfg, .ini, .env)
    :cvar BINARY: Binary files (.bin, .exe, .dll)
    :cvar TYPESCRIPT: TypeScript files (.ts, .tsx)
    :cvar UNKNOWN: Unknown file types
    """
    # Code files
    PYTHON = "python"          # .py, .pyx, .pyi, .pyc
    JAVASCRIPT = "javascript"  # .js, .jsx
    TYPESCRIPT = "typescript"  # .ts, .tsx
    JAVA = "java"             # .java, .class, .jar
    CPP = "cpp"               # .cpp, .cc, .cxx, .hpp, .h
    CSHARP = "csharp"         # .cs, .cshtml
    GO = "go"                 # .go
    RUST = "rust"             # .rs
    PHP = "php"               # .php, .phtml
    RUBY = "ruby"             # .rb, .erb
    SWIFT = "swift"           # .swift
    KOTLIN = "kotlin"         # .kt, .kts
    SCALA = "scala"           # .scala
    R = "r"                   # .r, .rmd
    SHELL = "shell"           # .sh, .bash, .zsh
    SQL = "sql"               # .sql, .psql, .mysql
    
    # Web files
    HTML = "html"             # .html, .htm, .xhtml
    CSS = "css"               # .css, .scss, .sass, .less
    XML = "xml"               # .xml, .xsl, .xslt
    JSON = "json"             # .json, .jsonl
    YAML = "yaml"             # .yml, .yaml
    
    # Document files
    MARKDOWN = "markdown"     # .md, .markdown
    TEXT = "text"            # .txt, .text
    PDF = "pdf"              # .pdf
    DOC = "doc"              # .doc, .docx
    EXCEL = "excel"          # .xls, .xlsx, .csv
    PPT = "powerpoint"       # .ppt, .pptx
    RTF = "rtf"              # .rtf
    TEX = "tex"              # .tex, .latex
    
    # Image files
    IMAGE = "image"          # .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp
    
    # Audio files
    AUDIO = "audio"          # .mp3, .wav, .ogg, .m4a, .flac
    
    # Video files
    VIDEO = "video"          # .mp4, .avi, .mov, .wmv, .flv, .webm
    
    # Archive files
    ARCHIVE = "archive"      # .zip, .tar, .gz, .7z, .rar
    
    # Data files
    CSV = "csv"              # .csv
    PARQUET = "parquet"      # .parquet
    HDF5 = "hdf5"           # .h5, .hdf5
    PICKLE = "pickle"        # .pkl, .pickle
    
    # Config files
    CONFIG = "config"        # .conf, .cfg, .ini, .env
    
    # Binary files
    BINARY = "binary"        # .bin, .exe, .dll
    
    # Other
    UNKNOWN = "unknown"      # Fallback for unknown types
    
    
    @classmethod
    @lru_cache(maxsize = 128)
    def from_extension(cls, extension: str) -> 'FileType':
        """Cached version to avoid repeated sync operations"""
        ext = extension.lower().lstrip('.')
        
        # Code files
        match ext:
            case 'py' | 'pyx' | 'pyi' | 'pyc':
                return cls.PYTHON
            case 'js' | 'jsx':
                return cls.JAVASCRIPT
            case 'ts' | 'tsx':
                return cls.TYPESCRIPT
            case 'java' | 'class' | 'jar':
                return cls.JAVA
            case 'cpp' | 'cc' | 'cxx' | 'hpp' | 'h':
                return cls.CPP
            case 'cs' | 'cshtml':
                return cls.CSHARP
            case 'go':
                return cls.GO
            case 'rs':
                return cls.RUST
            case 'php' | 'phtml':
                return cls.PHP
            case 'rb' | 'erb':
                return cls.RUBY
            case 'swift':
                return cls.SWIFT
            case 'kt' | 'kts':
                return cls.KOTLIN
            case 'scala':
                return cls.SCALA
            case 'r' | 'rmd':
                return cls.R
            case 'sh' | 'bash' | 'zsh':
                return cls.SHELL
            case 'sql' | 'psql' | 'mysql':
                return cls.SQL
            case 'html' | 'htm' | 'xhtml':
                return cls.HTML
            case 'css' | 'scss' | 'sass' | 'less':
                return cls.CSS
            case 'xml' | 'xsl' | 'xslt':
                return cls.XML
            case 'json' | 'jsonl':
                return cls.JSON
            case 'yml' | 'yaml':
                return cls.YAML
            case 'md' | 'markdown':
                return cls.MARKDOWN
            case 'txt' | 'text':
                return cls.TEXT
            case 'pdf':
                return cls.PDF
            case 'doc' | 'docx':
                return cls.DOC
            case 'xls' | 'xlsx':
                return cls.EXCEL
            case 'ppt' | 'pptx':
                return cls.PPT
            case 'rtf':
                return cls.RTF
            case 'tex' | 'latex':
                return cls.TEX
            case 'jpg' | 'jpeg' | 'png' | 'gif' | 'bmp' | 'svg' | 'webp':
                return cls.IMAGE
            case 'mp3' | 'wav' | 'ogg' | 'm4a' | 'flac':
                return cls.AUDIO
            case 'mp4' | 'avi' | 'mov' | 'wmv' | 'flv' | 'webm':
                return cls.VIDEO
            case 'zip' | 'tar' | 'gz' | '7z' | 'rar':
                return cls.ARCHIVE
            case 'csv':
                return cls.CSV
            case 'parquet':
                return cls.PARQUET
            case 'h5' | 'hdf5':
                return cls.HDF5
            case 'pkl' | 'pickle':
                return cls.PICKLE
            case 'conf' | 'cfg' | 'ini' | 'env':
                return cls.CONFIG
            case 'bin' | 'exe' | 'dll':
                return cls.BINARY
            
        return cls.UNKNOWN
