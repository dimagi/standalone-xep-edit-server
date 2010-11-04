function(doc) {
    if(doc.doc_type == "EditSession" && doc.active) {
        emit(doc.token, doc);
    }
}