'use client'

import useSWR from 'swr'

/**
 * Thin SWR wrapper so pages can consume the typed api-client with
 * consistent loading / error / data semantics. The `key` is only used
 * for caching + dedupe; `fetcher` calls into lib/api-client.
 */
export function useApi<T>(key: string, fetcher: () => Promise<T>) {
  const { data, error, isLoading, mutate } = useSWR<T>(key, fetcher, {
    revalidateOnFocus: false,
  })
  return { data, error, isLoading, mutate }
}
