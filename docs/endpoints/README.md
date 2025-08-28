# NAKALA API Endpoints - O-Nakala Core Documentation

## 🎯 Important: CSV vs Official API Format

### **O-Nakala Core Design Philosophy**

**O-Nakala Core provides user-friendly CSV abstractions** that differ intentionally from the official NAKALA API format. This is a **feature, not a bug**.

| Aspect | Official NAKALA API | O-Nakala Core CSV |
|--------|-------------------|------------------|
| **Creator Format** | `[{"givenname": "Jean", "surname": "Dupont"}]` | `"Dupont,Jean"` |
| **Multilingual** | Multiple separate API calls | `"fr:Titre\|en:Title"` |
| **Arrays** | JSON array structures | `"item1;item2;item3"` |
| **Complexity** | Raw API power | User-friendly simplicity |

### **Why Different Formats?**

1. **Ease of Use**: CSV `"Dupont,Jean"` vs JSON `[{"givenname": "Jean", "surname": "Dupont"}]`
2. **Batch Operations**: One CSV file vs hundreds of API calls
3. **Non-Technical Users**: Researchers can use Excel/LibreOffice
4. **Error Reduction**: Simple formats reduce syntax errors

### **Conversion Process**

```
📊 CSV Input → 🔄 O-Nakala Core → 📡 Official NAKALA API
User-Friendly     Transformation     Correct JSON
```

**Your CSV data is automatically converted to proper API format** - you get simplicity while maintaining full API compliance.

### **Official API Compatibility**

- ✅ **All API calls** use official NAKALA endpoints
- ✅ **All JSON payloads** match official API specification  
- ✅ **All responses** follow official API format
- ✅ **No API functionality** is lost or modified

**You get both**: User-friendly input **AND** full API compliance.

---

## 📚 Endpoint Documentation

### Core Endpoints
- **[Upload Endpoint](upload-endpoint/)** - Dataset creation and file upload
- **[Collection Endpoint](collection-endpoint/)** - Data organization and collections  
- **[Curator Endpoint](curator-endpoint/)** - Metadata enhancement and quality management

### Reference Materials
- **[Test API Documentation](https://apitest.nakala.fr/doc)** - Interactive NAKALA test API (Swagger/OpenAPI)
- **[Production API Documentation](https://api.nakala.fr/doc)** - Interactive NAKALA production API (Swagger/OpenAPI)
- **[Official NAKALA Documentation](https://documentation.huma-num.fr/nakala/)** - Complete platform documentation
- **[Data Preparation Guide](https://documentation.huma-num.fr/nakala-preparer-ses-donnees/)** - Official guide for preparing research data
- **[Metadata Description Guide](https://documentation.huma-num.fr/nakala-guide-de-description/)** - Official Dublin Core metadata specifications
- **[Field Reference](../curator-field-reference.md)** - Complete metadata field guide

---

## 🔗 Relationship to Official Documentation

### **When to Use Which Documentation**

| Task | Use This Documentation |
|------|----------------------|
| **Using o-nakala-core** | This documentation (CSV formats, CLI commands) |
| **Understanding NAKALA concepts** | [Official NAKALA Guide](../official-documentations/nakala-guide-de-description.md) |
| **Direct API development** | [Official API Spec](../official-documentations/apitest-nakala.json) |
| **Metadata standards** | Both (concepts from official, CSV format from ours) |

### **Complementary, Not Competing**

- **Official NAKALA docs**: Explain concepts, standards, raw API
- **O-Nakala Core docs**: Show how to accomplish tasks with user-friendly tools

Both are valuable for different purposes!

---

## 🎓 Learning Path

1. **Start here**: Understand CSV abstraction vs raw API
2. **Try examples**: Use working CSV files in `/examples/`
3. **Read official guide**: Understand NAKALA metadata concepts  
4. **Advanced usage**: Combine both approaches as needed

**Remember**: O-Nakala Core handles the complexity so you can focus on your research data.