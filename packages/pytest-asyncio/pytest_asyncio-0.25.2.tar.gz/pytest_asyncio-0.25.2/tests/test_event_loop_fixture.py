from __future__ import annotations

from textwrap import dedent

from pytest import Pytester


def test_event_loop_fixture_respects_event_loop_policy(pytester: Pytester):
    pytester.makeconftest(
        dedent(
            """\
            '''Defines and sets a custom event loop policy'''
            import asyncio
            from asyncio import DefaultEventLoopPolicy, SelectorEventLoop

            class TestEventLoop(SelectorEventLoop):
                pass

            class TestEventLoopPolicy(DefaultEventLoopPolicy):
                def new_event_loop(self):
                    return TestEventLoop()

            # This statement represents a code which sets a custom event loop policy
            asyncio.set_event_loop_policy(TestEventLoopPolicy())
            """
        )
    )
    pytester.makepyfile(
        dedent(
            """\
            '''Tests that any externally provided event loop policy remains unaltered'''
            import asyncio

            import pytest


            @pytest.mark.asyncio
            async def test_uses_loop_provided_by_custom_policy():
                '''Asserts that test cases use the event loop
                provided by the custom event loop policy'''
                assert type(asyncio.get_event_loop()).__name__ == "TestEventLoop"


            @pytest.mark.asyncio
            async def test_custom_policy_is_not_overwritten():
                '''
                Asserts that any custom event loop policy stays the same
                across test cases.
                '''
                assert type(asyncio.get_event_loop()).__name__ == "TestEventLoop"
            """
        )
    )
    result = pytester.runpytest_subprocess("--asyncio-mode=strict")
    result.assert_outcomes(passed=2)


def test_event_loop_fixture_handles_unclosed_async_gen(
    pytester: Pytester,
):
    pytester.makeini("[pytest]\nasyncio_default_fixture_loop_scope = function")
    pytester.makepyfile(
        dedent(
            """\
            import asyncio
            import pytest

            pytest_plugins = 'pytest_asyncio'

            @pytest.mark.asyncio
            async def test_something():
                async def generator_fn():
                    yield
                    yield

                gen = generator_fn()
                await gen.__anext__()
            """
        )
    )
    result = pytester.runpytest_subprocess("--asyncio-mode=strict", "-W", "default")
    result.assert_outcomes(passed=1, warnings=0)
