namespace iota
{
    class buffer_generator {
    public:
        buffer_generator(): vec(iota::create_vector<uint8_t>()) {}

        template<typename T>
        void add(index_type i, T item);

        void serialize(){
            // Just do NOP but let other APIs do the memory allocation here if they wish
            return;
        }

        uint8_t* data(){
            return vec.data();
        }

        size_t length(){
            return vec.size();
        }

    private:
        iota::vector<uint8_t> vec;
    };


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

        uint8_t raw = (uint8_t)item;
        vec.push_back(raw);
    }

    template<>
    void buffer_generator::add<int16_t>(index_type i, int16_t item){
        // int16 ::= index, word
        vec.push_back(i);

        uint16_t raw = (uint16_t)item;
        vec.push_back(raw & 0xFF);
        vec.push_back((raw >> 8) & 0xFF);
    }

    template<>
    void buffer_generator::add<int32_t>(index_type i, int32_t item){
        // int32 ::= index, dword
        vec.push_back(i);

        uint32_t raw = (uint32_t)item;
        vec.push_back(raw & 0xFF);
        vec.push_back((raw >> 8) & 0xFF);
        vec.push_back((raw >> 16) & 0xFF);
        vec.push_back((raw >> 24) & 0xFF);
    }

    template<>
    void buffer_generator::add<int64_t>(index_type i, int64_t item){
        // int64 ::= index, qword
        vec.push_back(i);

        uint64_t raw = (uint64_t)item;
        vec.push_back(raw & 0xFF);
        vec.push_back((raw >> 8) & 0xFF);
        vec.push_back((raw >> 16) & 0xFF);
        vec.push_back((raw >> 24) & 0xFF);
        vec.push_back((raw >> 32) & 0xFF);
        vec.push_back((raw >> 40) & 0xFF);
        vec.push_back((raw >> 48) & 0xFF);
        vec.push_back((raw >> 56) & 0xFF);
    }

    template<>
    void buffer_generator::add<iota::string>(index_type i, iota::string item){
        /*
         * string ::= index, string_length, {char}
         * string_length ::= qword
         */
        
        vec.push_back(i); // index

        // string_length
        uint64_t length = item.size();
        vec.push_back(length & 0xFF);
        vec.push_back((length >> 8) & 0xFF);
        vec.push_back((length >> 16) & 0xFF);
        vec.push_back((length >> 24) & 0xFF);
        vec.push_back((length >> 32) & 0xFF);
        vec.push_back((length >> 40) & 0xFF);
        vec.push_back((length >> 48) & 0xFF);
        vec.push_back((length >> 56) & 0xFF);

        // {char}
        for(size_t i = 0; i < length; i++)
            vec.push_back(item.data()[i]);
    }

    template<>
    void buffer_generator::add<iota::vector<uint8_t>>(index_type i, iota::vector<uint8_t> item){
        /*
         * buffer ::= index, buffer_length, {byte}
         * buffer_length ::= qword
         */
        
        vec.push_back(i); // index

        // buffer_length
        uint64_t length = item.size();
        vec.push_back(length & 0xFF);
        vec.push_back((length >> 8) & 0xFF);
        vec.push_back((length >> 16) & 0xFF);
        vec.push_back((length >> 24) & 0xFF);
        vec.push_back((length >> 32) & 0xFF);
        vec.push_back((length >> 40) & 0xFF);
        vec.push_back((length >> 48) & 0xFF);
        vec.push_back((length >> 56) & 0xFF);

        // {byte}
        for(size_t i = 0; i < length; i++)
            vec.push_back(item.data()[i]);
    }

    template<>
    void buffer_generator::add<iota::vector<uint64_t>>(index_type i, iota::vector<uint64_t> item){
        /*
         * list ::= index, list_length, {qword}
         * list_length ::= qword
         */
        
        vec.push_back(i); // index

        // list_length
        uint64_t length = item.size();
        vec.push_back(length & 0xFF);
        vec.push_back((length >> 8) & 0xFF);
        vec.push_back((length >> 16) & 0xFF);
        vec.push_back((length >> 24) & 0xFF);
        vec.push_back((length >> 32) & 0xFF);
        vec.push_back((length >> 40) & 0xFF);
        vec.push_back((length >> 48) & 0xFF);
        vec.push_back((length >> 56) & 0xFF);

        // {qword}
        for(size_t i = 0; i < length; i++){
            auto entry = item.data()[i];
            vec.push_back(entry & 0xFF);
            vec.push_back((entry >> 8) & 0xFF);
            vec.push_back((entry >> 16) & 0xFF);
            vec.push_back((entry >> 24) & 0xFF);
            vec.push_back((entry >> 32) & 0xFF);
            vec.push_back((entry >> 40) & 0xFF);
            vec.push_back((entry >> 48) & 0xFF);
            vec.push_back((entry >> 56) & 0xFF);
        }
    }
         
} // namespace iota
