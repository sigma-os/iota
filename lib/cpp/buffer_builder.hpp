namespace iota
{
    class buffer_generator {
    public:

    template<typename T>
    void add(index_type i, T item);

    void serialize(){
        // Just do NOP but let other APIs do the memory allocation here if they wish
        return;
    }

    uint8_t* data(){
        return vec.data();
    }
    private:
        iota::vector<uint8_t> vec;
    };

    template<typename T>
    void buffer_generator::add<T>(index_type i, T item){ }

    template<>
    void buffer_generator::add<uint8_t>(index_type i, uint8_t item){
        // uint8 ::= index, byte
        vec.push_back(i);
        vec.push_back(item);
    }

    template<>
    void buffer_generator::add<uint16_t>(index_type i, uint16_t item){
        // uint16 ::= index, word
        vec.push_back(i);
        vec.push_back(item & 0xFF);
        vec.push_back((item >> 8) & 0xFF);
    }

    template<>
    void buffer_generator::add<uint32_t>(index_type i, uint32_t item){
        // uint32 ::= index, dword
        vec.push_back(i);
        vec.push_back(item & 0xFF);
        vec.push_back((item >> 8) & 0xFF);
        vec.push_back((item >> 16) & 0xFF);
        vec.push_back((item >> 24) & 0xFF);
    }

    template<>
    void buffer_generator::add<uint64_t>(index_type i, uint64_t item){
        // uint64 ::= index, qword
        vec.push_back(i);
        vec.push_back(item & 0xFF);
        vec.push_back((item >> 8) & 0xFF);
        vec.push_back((item >> 16) & 0xFF);
        vec.push_back((item >> 24) & 0xFF);
        vec.push_back((item >> 32) & 0xFF);
        vec.push_back((item >> 40) & 0xFF);
        vec.push_back((item >> 48) & 0xFF);
        vec.push_back((item >> 56) & 0xFF);
    }

    template<>
    void buffer_generator::add<int8_t>(index_type i, int8_t item){
        // int8 ::= index, byte
        vec.push_back(i);
        vec.push_back(item);
    }

    template<>
    void buffer_generator::add<int16_t>(index_type i, int16_t item){
        // int16 ::= index, word
        vec.push_back(i);
        vec.push_back(item & 0xFF);
        vec.push_back((item >> 8) & 0xFF);
    }

    template<>
    void buffer_generator::add<int32_t>(index_type i, int32_t item){
        // int32 ::= index, dword
        vec.push_back(i);
        vec.push_back(item & 0xFF);
        vec.push_back((item >> 8) & 0xFF);
        vec.push_back((item >> 16) & 0xFF);
        vec.push_back((item >> 24) & 0xFF);
    }

    template<>
    void buffer_generator::add<int64_t>(index_type i, int64_t item){
        // int64 ::= index, qword
        vec.push_back(i);
        vec.push_back(item & 0xFF);
        vec.push_back((item >> 8) & 0xFF);
        vec.push_back((item >> 16) & 0xFF);
        vec.push_back((item >> 24) & 0xFF);
        vec.push_back((item >> 32) & 0xFF);
        vec.push_back((item >> 40) & 0xFF);
        vec.push_back((item >> 48) & 0xFF);
        vec.push_back((item >> 56) & 0xFF);
    }
} // namespace iota
