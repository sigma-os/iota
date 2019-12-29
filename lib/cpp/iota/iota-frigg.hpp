#pragma once

#include <stdint.h>
#include <frg/optional.hpp>
#include <frg/vector.hpp>
#include <frg/string.hpp>

#ifndef IOTA_FRIGG_ALLOCATOR
#error "IOTA_FRIGG_ALLOCATOR isn't set"
#endif

#ifndef IOTA_FRIGG_GET_ALLOCATOR
#error "IOTA_FRIGG_GET_ALLOCATOR isn't set"
#endif

namespace iota
{
    using index_type = uint8_t;

    template<typename T>
    using optional = frg::optional<T>;

    template<typename T>
    optional<T> create_optional(){
        return {};
    }

    template<typename T>
    using vector = frg::vector<T, IOTA_FRIGG_ALLOCATOR>;

    template<typename T>
    vector<T> create_vector(){
        return vector<T>{IOTA_FRIGG_GET_ALLOCATOR()};
    }

    using string = frg::string<IOTA_FRIGG_ALLOCATOR>;

    string create_string(){
        return string{IOTA_FRIGG_GET_ALLOCATOR()};
    }
} // namespace iota

#define IOTA_LIB_AVAILABLE