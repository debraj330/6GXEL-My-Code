set(SOURCES consumer.cc producer.cc parse_config.cc)
set(ZMQ_COMPILE_FLAGS "-lzmq")
set(THREAD_LIB "-pthread")

add_library(scale_ric_agent STATIC ${SOURCES} )
target_link_libraries(scale_ric_agent ${ZMQ_COMPILE_FLAGS}
                ${THREAD_LIB})
