namespace iota
{
    template<typename T>
    size_t parse_item(uint8_t* data, T& value);

    template<>
    size_t parse_item<uint8_t>(uint8_t* data, uint8_t& value){
        using T = uint8_t;
        value = (T)data[0];
        return 1;
    }

    template<>
    size_t parse_item<uint16_t>(uint8_t* data, uint16_t& value){
        using T = uint16_t;
        value = (T)data[0] | ((T)data[1] << 8);
        return 2;
    }

    template<>
    size_t parse_item<uint32_t>(uint8_t* data, uint32_t& value){
        using T = uint32_t;
        value = (T)data[0] | ((T)data[1] << 8) | ((T)data[2] << 16) | ((T)data[3] << 24);
        return 4;
    }

    template<>
    size_t parse_item<uint64_t>(uint8_t* data, uint64_t& value){
        using T = uint64_t;
        value = (T)data[0] | ((T)data[1] << 8) | ((T)data[2] << 16) | ((T)data[3] << 24) | ((T)data[4] << 32) | ((T)data[5] << 40) | ((T)data[6] << 48) | ((T)data[7] << 56);
        return 8;
    }

    template<>
    size_t parse_item<int8_t>(uint8_t* data, int8_t& value){
        using T = int8_t;
        value = (T)data[0];
        return 1;
    }

    template<>
    size_t parse_item<int16_t>(uint8_t* data, int16_t& value){
        using T = uint16_t;
        value = (uint16_t)((T)data[0] | ((T)data[1] << 8));
        return 2;
    }

    template<>
    size_t parse_item<int32_t>(uint8_t* data, int32_t& value){
        using T = uint32_t;
        value = (int32_t)((T)data[0] | ((T)data[1] << 8) | ((T)data[2] << 16) | ((T)data[3] << 24));
        return 4;
    }

    template<>
    size_t parse_item<int64_t>(uint8_t* data, int64_t& value){
        using T = uint64_t;
        value = (int64_t)((T)data[0] | ((T)data[1] << 8) | ((T)data[2] << 16) | ((T)data[3] << 24) | ((T)data[4] << 32) | ((T)data[5] << 40) | ((T)data[6] << 48) | ((T)data[7] << 56));
        return 8;
    }


    template<>
    size_t parse_item<iota::string>(uint8_t* data, iota::string& value){
        using T = uint64_t;
        size_t size = (T)data[0] | ((T)data[1] << 8) | ((T)data[2] << 16) | ((T)data[3] << 24) | ((T)data[4] << 32) | ((T)data[5] << 40) | ((T)data[6] << 48) | ((T)data[7] << 56);
        value.resize(size);
        for(size_t i = 0; i < size; i++)
            value[i] = data[8 + i];

        return 8 + size;
    }

    template<>
    size_t parse_item<iota::vector<uint8_t>>(uint8_t* data, iota::vector<uint8_t>& value){
        using T = uint64_t;
        size_t size = (T)data[0] | ((T)data[1] << 8) | ((T)data[2] << 16) | ((T)data[3] << 24) | ((T)data[4] << 32) | ((T)data[5] << 40) | ((T)data[6] << 48) | ((T)data[7] << 56);
        value.resize(size * sizeof(uint8_t));
        for(size_t i = 0; i < size; i++)
            value[i] = data[8 + i];

        return 8 + (size * sizeof(uint8_t));
    }

    template<>
    size_t parse_item<iota::vector<uint64_t>>(uint8_t* data, iota::vector<uint64_t>& value){
        using T = uint64_t;
        size_t size = (T)data[0] | ((T)data[1] << 8) | ((T)data[2] << 16) | ((T)data[3] << 24) | ((T)data[4] << 32) | ((T)data[5] << 40) | ((T)data[6] << 48) | ((T)data[7] << 56);
        value.resize(size);
        for(size_t i = 0; i < size; i++)
            value[i] = (T)data[8 + (i * 8)] | ((T)data[8 + (i * 8) + 1] << 8) | ((T)data[8 + (i * 8) + 2] << 16) | ((T)data[8 + (i * 8) + 3] << 24) | ((T)data[8 + (i * 8) + 4] << 32) | ((T)data[8 + (i * 8) + 5] << 40) | ((T)data[8 + (i * 8) + 6] << 48) | ((T)data[8 + (i * 8) + 7] << 56);;

        return 8 + (size * sizeof(uint64_t));
    }
} // namespace iota
